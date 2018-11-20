from django import template


register = template.Library()


@register.filter
def escape_quotation_marks(value):
    '''
    Replaces all quotation marks with escaped quotation marks. Without this
    filter, unescaped text put into JavaScript quotes (e.g. when setting the
    value of an input), will break the quote and cause an error if user input
    includes the same type of quotation mark.
    '''
    print(value.replace("'", "\\'").replace('"', '"').replace('\\`', '\\`'))
    return value.replace("'", "\\'").replace('"', '"').replace('\\`', '\\`')
