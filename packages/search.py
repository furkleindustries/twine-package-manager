from django.contrib.postgres import search

from packages.models import Package


def packages_search_filter(query, queryset):
    models = queryset
    if not models:
        models = Package.objects.all()

    vector = search.SearchVector('name', 'description', 'keywords')
    search_query = search.SearchQuery(query)
    rank = search.SearchRank(vector, query)

    # Get results that contain the search in the name.
    return models.annotate(rank=rank).order_by('-rank')
