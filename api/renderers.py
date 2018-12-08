from rest_framework.renderers import TemplateHTMLRenderer


class ContextAwareTemplateHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        if response.exception:
            data['status_code'] = response.status_code
            return data
        else:
            context = {}
            if 'results' in data:
                context = data
            else:
                context['item'] = data

            # pop keys which we do not need in the template
            keys_to_delete = ['request', 'response', 'args', 'kwargs']
            for item in keys_to_delete:
                renderer_context.pop(item)

            for key, value in renderer_context.items():
                if key not in context:
                    context[key] = value

            return context
