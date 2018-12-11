from django.views import generic

from .models import Profile

from api.renderers import ContextAwareTemplateHTMLRenderer
from api.views import ProfileDetailRetrieveOnly
from packages.models import Package


class DetailView(ProfileDetailRetrieveOnly):
    renderer_classes = (ContextAwareTemplateHTMLRenderer,)
    template_name = 'profiles/detail.html'

    def get_renderer_context(self):
        context = super().get_renderer_context()

        user = context.get('user')

        context['packages'] = Package.objects.filter(owner_id=user.id)
        context['profile'] = user.profile
        context['with_labels'] = True
        context['with_dates'] = True
        return context
