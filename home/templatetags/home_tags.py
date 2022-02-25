from django import template
register = template.Library()
#from ..models import Contact

# @register.simple_tag
# def total_classes():
#     return Class.objects.all().count()

# @register.simple_tag
# def total_pupils():
#     return Pupil.objects.all().count()

@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url
