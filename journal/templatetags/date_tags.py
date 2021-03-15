from django import template
from journal.models import WorkDays

register = template.Library()


@register.simple_tag
def get_last_date():
    query = WorkDays.objects.all().order_by('-day')[0]
    return query.day
