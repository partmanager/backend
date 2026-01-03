from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 1000