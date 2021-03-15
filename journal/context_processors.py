from .models import STATUS_CHOICES
from users.models import Officer


def status_processor(request):
    statuses = []
    officers = Officer.objects.all()
    for key, value in STATUS_CHOICES:
        statuses.append(value)

    return {
        'statuses': statuses,
        'officers': officers
    }
