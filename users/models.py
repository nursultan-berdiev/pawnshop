from django.db import models
from django.contrib.auth.models import User


def name_user(str):
    need_officer = Officer.objects.filter(name=str)[0]
    our_user = need_officer.user
    return our_user


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='ФИО Сотрудника')

    def __str__(self):
        return self.name
