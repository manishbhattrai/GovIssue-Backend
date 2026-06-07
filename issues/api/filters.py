import django_filters
from issues.models import Issue

class IssueFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')

    class Meta:
        model = Issue
        fields = ['category','status']
