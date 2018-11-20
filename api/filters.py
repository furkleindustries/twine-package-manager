from rest_framework import filters

from packages.search import packages_search_filter


class PackageSearchFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        query = request.GET.get('query')

        word_rule = request.GET.get('word_rule') or '|'

        search_results = packages_search_filter(query, queryset,
                                                word_rule=word_rule,
                                                quantity=-1)

        return search_results
