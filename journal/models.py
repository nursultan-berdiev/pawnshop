from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Officer

STATUS_CHOICES = (
    ('Выдан', 'Выдан'),
    ('Просрочен', 'Просрочен'),
    ('Продлен', 'Продлен'),
    ('Выкуп', 'Выкуп'),
    ('Реализован', 'Реализован'),
)


def one_day_more():
    return timezone.now() + timezone.timedelta(days=1)


def next_number():
    if Loan.objects.all().count() == 0:
        return 1
    else:
        last_loan = Loan.objects.order_by('-nomer_bileta')[0]
        number = last_loan.nomer_bileta
        return number + 1


class Client(models.Model):
    client_name = models.CharField(max_length=50, verbose_name='ФИО клиента')
    phone_number = models.CharField(max_length=10, verbose_name='Номер телефона')
    phone_number_reserve = models.CharField(max_length=10, verbose_name='Доп. номер телефона')
    comment = models.TextField(null=True, verbose_name='Комментарий по клиенту')

    def __str__(self):
        return self.client_name


class Zalog_types(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип залога')

    def __str__(self):
        return self.type


class Zalog(models.Model):
    zalog_name = models.ForeignKey(Zalog_types, on_delete=models.CASCADE, verbose_name='Тип залога')
    description = models.TextField(verbose_name='Описание залога')
    price = models.FloatField(verbose_name='Оценка Залога')
    sell_price = models.FloatField(verbose_name='Цена Реализации')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    def __str__(self):
        return self.description


class Loan(models.Model):
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата заявки')
    nomer_bileta = models.IntegerField(unique=True, default=next_number, verbose_name='Номер заявки')
    fio_klienta = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='ФИО клиента')
    summa_zayavki = models.IntegerField(null=False, verbose_name='Сумма заявки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    stavka_day = models.FloatField(null=True, verbose_name='Процентная ставка в день')
    srok_kredita = models.IntegerField(null=False, verbose_name='Срок займа в днях')
    comment = models.TextField(null=True, blank=True, verbose_name='Дополнительные комментарии')

    ostatok = models.FloatField(null=True, default=summa_zayavki, verbose_name='Остаток основной суммы')
    stavka_period = models.FloatField(null=True, verbose_name='Ожидаемый доход за период')
    expected_stavka_day = models.FloatField(null=True, verbose_name='Ожидаемый доход в день')
    fact_day = models.FloatField(null=True, default=0, verbose_name='Начисленные проценты')
    itogo_k_vyplate = models.FloatField(null=True, default=ostatok, verbose_name='Итого к выплате')
    fact_loan_day = models.IntegerField(null=False, default=0, verbose_name='Количество фактических дней')
    date_plan_pay = models.DateTimeField(null=False, blank=False, verbose_name='Дата окончания')
    date_fact_pay = models.DateTimeField(null=True, blank=True, verbose_name='Дата фактического окончания')
    zalog = models.OneToOneField(Zalog, on_delete=models.CASCADE, primary_key=True,
                                 verbose_name='Наименование залога')
    credit_user = models.ForeignKey(Officer, on_delete=models.SET('Удаленный пользователь'),
                                    verbose_name='Кредитный специалист')

    def __str__(self):
        return self.fio_klienta

    def save(self, *args, **kwargs):
        if self.srok_kredita or self.date_posted is None:
            return 'Введите срок и начало кредита'
        else:
            self.date_plan_pay = self.date_posted + timezone.timedelta(days=self.srok_kredita)
            super().save(*args, **kwargs)

        if self.summa_zayavki and self.srok_kredita and self.date_posted and self.stavka_day is not None:
            self.stavka_period = self.stavka_day / 100 * self.ostatok * self.srok_kredita
            self.expected_stavka_day = self.stavka_day / 100 * self.ostatok
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'pk': self.pk})
