from re import split

from django.contrib.postgres import search
from django.db.models import F, Func, Value

from packages.models import Package


def packages_search_filter(query, queryset, word_rule='|'):
    nice_query = split(r'\s', query.strip())

    models = queryset
    if not models:
        models = Package.objects.all()

    vector = search.SearchVector('name', weight='A')
    vector += search.SearchVector(Func(F('keywords'), Value(' '),
                                       function='array_to_string'),
                                  weight='B')

    vector += search.SearchVector('description', weight='B')

    search_query = search.SearchQuery(nice_query[0])
    for ii in range(1, len(nice_query)):
        subquery = nice_query[ii]
        if word_rule == '&':
            search_query &= search.SearchQuery(subquery)
        else:
            search_query |= search.SearchQuery(subquery)

    rank = search.SearchRank(vector, search_query)
    annotated = models.annotate(rank=rank).order_by('-rank')

    # Grab all exact (case-insensitive) name matches to the query. This is
    # necessary for very short package names.
    name_pass = annotated.filter(name__iexact=query)

    # Filter out all non-exact matches below rank 0.05.
    rank_high_pass = annotated.filter(rank__gt=0)
    results = name_pass.union(rank_high_pass)[0:100]

    return results
