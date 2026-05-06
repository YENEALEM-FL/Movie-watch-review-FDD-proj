from rest_framework.pagination import (CursorPagination, LimitOffsetPagination,
                                       PageNumberPagination)


class WatchListPagination(PageNumberPagination):
    page_size = 2 # specify the number of items to be displayed on a page
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size  = 10
    last_page_strings = 'end'


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCPagination(CursorPagination):
    page_size = 2
    ordering = 'created'
    cursor_query_param = 'record'
