from re import split

from django.contrib.postgres import search
from django.db.models import F, Func, Value

from packages.models import Package


def packages_search_filter(query, queryset, word_rule='&', quantity=10):
    # Split the query into whitespace-separated subqueries, each of which will
    # either be queried together or separately, depending on the options.
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
        if word_rule == '&':
            search_query &= search.SearchQuery(nice_query[ii])
        else:
            search_query |= search.SearchQuery(nice_query[ii])

    rank = search.SearchRank(vector, search_query)
    annotated = models.annotate(rank=rank).order_by('-rank')

    # Grab any exact (case-insensitive) name match to the query. This is
    # necessary for very short package names.
    name_pass = annotated.filter(name__iexact=query)

    # Filter out all rank 0 results.
    rank_high_pass = annotated.filter(rank__gt=0)

    # Add the exact match at the front, if it exists.
    results = name_pass.union(rank_high_pass)

    # Restrict the number of results to the quantity argument.
    if quantity != -1:
        results = results[0:quantity]

    return results
