from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, viewsets, status
from rest_framework.parsers import MultiPartParser,FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, F, Avg
from .serializers import (

CategorySerializer,
CreateIssueSerializer, ListIssueSerializer,
RetrieveUpdateIssueSerializer,

)
from .permissions import IsOwnerOrReadOnly
from issues.models import Category, Issue
from .filters import IssueFilter
from .pagination import MyIssuePagination, IssuePagination
from .throttles import UpdateIssueThrottle


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('created_at')
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permission(self):

        if self.request.method in ['GET','HEAD','OPTIONS']:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


class ListCreateIssueView(generics.ListCreateAPIView):


    serializer_class = ListIssueSerializer
    parser_classes = [MultiPartParser,FormParser]
    filterset_class = IssueFilter
    pagination_class = IssuePagination

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateIssueSerializer

        return ListIssueSerializer

    def get_queryset(self):

        user=self.request.user

        if user.is_staff:
            issue = (Issue.objects.select_related('category','created_by')
                 .prefetch_related('location')
                 .order_by('-created_at')
                 )

        else:
            issue = (Issue.objects.select_related('category','created_by')
                 .prefetch_related('location')
                 .exclude(Q(created_by=user) | Q(status='p'))
                 .order_by('-created_at')
                 )
        return issue


    def perform_create(self,serializer):

        user = self.request.user
        if user.trust_points >= 250:

            issue = serializer.save(created_by=user, status='v', verified_point_awarded=True)
            user.trust_points += 10
            user.save()

        else:
            issue = serializer.save(created_by=user)


class ListOwnIssueView(generics.ListAPIView):

    serializer_class = ListIssueSerializer
    filterset_fields = ['category','status']
    pagination_class = MyIssuePagination

    def get_queryset(self):
        user = self.request.user
        issue = (Issue.objects.select_related('category','created_by')
                 .prefetch_related('location')
                 .filter(created_by=user)
                 .order_by('created_at')
                 )
        return issue


class RetrieveUpdateIssueView(generics.RetrieveUpdateAPIView):

    queryset = Issue.objects.select_related('category','created_by').prefetch_related('location')
    serializer_class = RetrieveUpdateIssueSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'issue_id'

    def get_throttles(self):
        if self.request.method in ["PUT","PATCH"]:
            return [UpdateIssueThrottle()]
        return super().get_throttles()

    def perform_update(self,serializer):

        instance = self.get_object()
        old_status = instance.status
        new_status = serializer.validated_data.get('status')

        from rest_framework.exceptions import ValidationError


        if old_status == 'r' and new_status in ['v','p','o','ip']:
            raise ValidationError("Resolved issues cannot be changed back to other status.")

        elif old_status == 'p' and new_status != 'v':
            raise ValidationError("Only verified status is available.")

        elif old_status in ['v','o','ip'] and new_status == 'p':
            raise ValidationError(" Status cannot be changed to pending.")

        updated_issue = serializer.save()

        if  new_status == 'v' and not updated_issue.verified_point_awarded:

            user = updated_issue.created_by
            user.trust_points += 10
            user.save()

            updated_issue.verified_point_awarded = True
            updated_issue.save()

        elif  new_status == 'r' and not updated_issue.resolved_point_awarded:

            user = updated_issue.created_by
            user.trust_points += 50
            user.save()
            updated_issue.resolved_point_awarded = True
            updated_issue.save()


class DashboardDataView(APIView):

    def get(self, request):
        user = request.user

        if user.is_staff:
            total_categories = Category.objects.count()
            total_issues = Issue.objects.count()
            resolved_issues = Issue.objects.filter(status='r')

            if resolved_issues.exists():
                avg_time = resolved_issues.annotate(
                    duration=F('updated_at') - F('created_at')
                ).aggregate(Avg('duration'))['duration__avg']
                avg_resolution_days = round(avg_time.total_seconds() / 86400, 1)
            else:
                avg_resolution_days = 0

            chart_queryset = (
                Issue.objects
                .values('status')
                .annotate(count=Count('id'))
            )
            pie_data = []
            for item in chart_queryset:
                percentage = round((item['count'] / total_issues) * 100, 2) if total_issues else 0
                pie_data.append({
                    "status": item['status'],
                    "count": item['count'],
                    "percentage": percentage
                })

            category_perf_queryset = (
                resolved_issues
                .values('category__name')
                .annotate(cat_avg=Avg(F('updated_at') - F('created_at')))
            )

            category_performance = []
            for item in category_perf_queryset:
                cat_avg_days = round(item['cat_avg'].total_seconds() / 86400, 1) if item['cat_avg'] else 0

                # Evaluation: Faster than global avg = high, slower = low
                if cat_avg_days < avg_resolution_days:
                    perf_label = "high"
                elif cat_avg_days > (avg_resolution_days + 1):
                    perf_label = "low"
                else:
                    perf_label = "normal"

                category_performance.append({
                    "name": item['category__name'],
                    "avg_days": cat_avg_days,
                    "performance": perf_label
                })

            dashboard_data = {
                "chart_type": "pie",
                "total_categories": total_categories,
                "total_issues": total_issues,
                "stats": pie_data,
                "avg_resolution_time": avg_resolution_days,
                "category_performance": category_performance
            }

        else:
            # User Dashboard Logic
            total_issues = Issue.objects.filter(created_by=user).count()
            bar_queryset = (
                Issue.objects
                .filter(created_by=user)
                .values('status')
                .annotate(count=Count('id'))
                .order_by('status')
            )

            labels = []
            data = []
            for item in bar_queryset:
                labels.append(item['status'])
                data.append(item['count'])

            dashboard_data = {
                "chart_type": "bar",
                "total_issues": total_issues,
                "stats": {
                    "labels": labels,
                    "data": data
                }
            }

        return Response(dashboard_data, status=status.HTTP_200_OK)