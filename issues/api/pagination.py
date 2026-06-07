from rest_framework.pagination import PageNumberPagination,CursorPagination


class MyIssuePagination(PageNumberPagination):

    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10


class IssuePagination(CursorPagination):

    page_size = 8
    ordering = '-created_at'


