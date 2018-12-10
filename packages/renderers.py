from api.renderers import ContextAwareTemplateHTMLRenderer

from profiles.models import Profile


def with_author(package):
    try:
        package['author'] = Profile.objects.get(user_id=package['author'])
    except Profile.DoesNotExist:
        pass

    return package


def with_owner(package):
    try:
        package['owner'] = Profile.objects.get(user_id=package['owner'])
    except Profile.DoesNotExist:
        pass

    return package


class PackageAuthorAwareTemplateHTMLRenderer(ContextAwareTemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            return data

        context = super().get_template_context(data, renderer_context)
        if 'results' in context:
            context['results'] = [with_author(x) for x in context['results']]
        else:
            context['item'] = with_author(context['item'])

        return context


class PackageOwnerAwareTemplateHTMLRenderer(ContextAwareTemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            return data

        context = super().get_template_context(data, renderer_context)
        if 'results' in context:
            context['results'] = [with_owner(x) for x in context['results']]
        else:
            context['item'] = with_owner(context['item'])

        return context


class PackageAuthorAndOwnerAwareTemplateHTMLRenderer(
    ContextAwareTemplateHTMLRenderer
):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            return data

        context = super().get_template_context(data, renderer_context)
        if 'results' in context:
            context['results'] = [
                with_author(with_owner(x)) for x in context['results']
            ]
        else:
            context['item'] = with_author(with_owner(context['item']))

        return context
