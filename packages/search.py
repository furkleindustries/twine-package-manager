from django.contrib.postgres import search
from django.db.models import F, Func, Value

from packages.models import Package


def packages_search_filter(query, queryset):
    nice_query = query.strip()

    models = queryset
    if not models:
        models = Package.objects.all()

    vector = search.SearchVector('name', weight='A')
    vector += search.SearchVector(Func(F('keywords'), Value(' '),
                                       function='array_to_string'),
                                  weight='C')

    vector += search.SearchVector('description', weight='D')

    search_query = search.SearchQuery(nice_query)
    rank = search.SearchRank(vector, search_query)
    annotated = models.annotate(rank=rank).order_by('-rank')

    # Grab all exact (case-insensitive) name matches to the query. This is
    # necessary for very short package names.
    name_pass = annotated.filter(name__iexact=nice_query)

    # Filter out all non-exact matches below rank 0.05.
    rank_high_pass = annotated.filter(rank__gte=0.05)
    results = name_pass.union(rank_high_pass)

    return results
