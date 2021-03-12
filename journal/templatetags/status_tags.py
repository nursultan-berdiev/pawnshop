from django import template
from journal.models import WorkDays, STATUS_CHOICES

register = template.Library()


@register.simple_tag
def get_status_color(status):
    if status == STATUS_CHOICES[0][0]:
        return 'success'
    elif status == STATUS_CHOICES[1][0]:
        return 'danger'
    elif status == STATUS_CHOICES[2][0]:
        return 'info'
    elif status == STATUS_CHOICES[3][0]:
        return 'primary'
    elif status == STATUS_CHOICES[4][0]:
        return 'warning'
    else:
        return 'secondary'
