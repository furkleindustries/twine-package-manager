from django.contrib.postgres import search
from django.db.models import F, Func, Value

from packages.models import Package


def packages_search_filter(query, queryset):
    models = queryset
    if not models:
        models = Package.objects.all()

    vector = search.SearchVector('name', weight='A')
    vector += search.SearchVector(Func(F('keywords'), Value(' '),
                                       function='array_to_string'),
                                  weight='B')

    vector += search.SearchVector('description', weight='C')

    search_query = search.SearchQuery(query)
    rank = search.SearchRank(vector, search_query)

    # Get results that contain the search in the name.
    return models.annotate(rank=rank).order_by('-rank').filter(rank__gte=0.1)
