from rest_framework import pagination, response


DEFAULT_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100
PAGE_SIZE_PARAM = 'page_size'


class PageSizeAwareCursorPagination(pagination.CursorPagination):
    page_size = DEFAULT_PAGE_SIZE
    max_page_size = MAX_PAGE_SIZE
    page_size_query_param = PAGE_SIZE_PARAM


class PageSizeAwareOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = DEFAULT_PAGE_SIZE
    max_limit = MAX_PAGE_SIZE
    limit_query_param = PAGE_SIZE_PARAM
