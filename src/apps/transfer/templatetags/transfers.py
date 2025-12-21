from django import template
from django.utils.safestring import mark_safe
import markdown

from .. import models


register = template.Library()


@register.simple_tag
def get_company_data():
    return models.CompanyData.load()


@register.simple_tag
def get_latest_tours():
    return models.Tour.objects.all()[:5]


@register.simple_tag
def get_media():
    return models.Media.objects.all()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def get_places():
    return models.Place.objects.all()
