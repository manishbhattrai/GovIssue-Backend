from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (

CategoryViewSet,
ListCreateIssueView, ListOwnIssueView,
RetrieveUpdateIssueView, DashboardDataView

)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [

    path('', include(router.urls)),
    path('issue/', ListCreateIssueView.as_view(), name='list-create-issues'),
    path('own/',ListOwnIssueView.as_view(), name='my-issue-list'),
    path('details/<uuid:issue_id>/', RetrieveUpdateIssueView.as_view(), name='issue-detail'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data')

]