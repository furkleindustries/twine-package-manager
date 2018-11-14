from packages.models import Package


def packages_search_filter(query, queryset):
    models = queryset
    if not models:
        models = Package.objects.all()

    nice_query = query.replace(',', '').replace('.', '')

    # Get results that contain the search in the name.
    return models.filter(name__icontains=nice_query).union(
                         # Add results that contain the search in the
                         # description.
                         models.filter(description__icontains=nice_query),
                         # Add results that contain the search in the keywords.
                         models.filter(keywords__icontains=nice_query))
