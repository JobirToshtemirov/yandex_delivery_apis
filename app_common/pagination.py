from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class for pagination.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'
