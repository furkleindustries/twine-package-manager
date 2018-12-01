from django.db.models import Count

from django.views import generic

from packages.models import Package


def trim_name(name):
    if len(name) > 37:
        return name[:37] + '...'

    return name


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'
    context_object_name = 'latest_packages'

    def get_queryset(self):
        return Package.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset().all()

        # Get the names of the ten most downloaded packages and restrict their
        # length to 40 characters or less.
        downloaded = queryset.annotate(
            downloads=Count('packagedownload')
        ).order_by(
            '-downloads'
        )[:10].values('name')

        # Get the names of the last ten published packages and restrict their
        # length to 40 characters or less.
        downloaded_names = [{'name': trim_name(x['name'])} for x in downloaded]

        newest = queryset.order_by('-date_created')[:10].values('name')
        newest_names = [{'name': trim_name(x['name'])} for x in newest]

        # Get the names of the last ten modified packages and restrict their
        # length to 40 characters or less.
        r_mods = queryset.order_by('-date_modified')[:10].values('name')
        r_mods_names = [{'name': trim_name(x['name'])} for x in r_mods]

        context.update({
            'package_links': True,
            'package_small_size': True,
            'most_downloaded_packages': downloaded_names,
            'newest_packages': newest_names,
            'recently_modified_packages': r_mods_names,
        })

        return context
