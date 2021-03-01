from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Officer

STATUS_CHOICES = (
    ('На рассмотрении', 'На рассмотрении'),
    ('Одобрено', 'Одобрено'),
    ('Отказано', 'Отказано'),
)

PURPOSE_CHOICES = (
    ('Потребительские', 'Потребительские'),
    ('Бизнес', 'Бизнес'),
)

ZALOG_CHOISES = (
    ('Заработная плата', 'Заработная плата'),
    ('Доход от бизнеса', 'Доход от бизнеса'),
    ('Поручительство', 'Поручительство'),
    ('Недвижимость', 'Недвижимость'),
    ('Движимое имущество', 'Движимое имущество'),
)

ISTOCHNIK_CHOISES = (
    ('Заработная плата', 'Заработная плата'),
    ('Доход от бизнеса', 'Доход от бизнеса'),
    ('Другие доходы', 'Другие доходы'),
)


def one_day_more():
    return timezone.now() + timezone.timedelta(days=1)


def next_number():
    if Client.objects.all().count() == 0:
        return 1
    else:
        last_client = Client.objects.order_by('-nomer_zayavki')[0]
        number = last_client.nomer_zayavki
        return number + 1


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='Продукт кредитования')
    interest_rate = models.FloatField(verbose_name='Процентная ставка', default=28)
    interest_rate_2 = models.FloatField(verbose_name='Процентная ставка вторая', null=True, blank=True)
    interest_rate_3 = models.FloatField(verbose_name='Процентная ставка третья', null=True, blank=True)
    sum = models.IntegerField(verbose_name='Сумма 1', default=100000)
    sum_2 = models.IntegerField(verbose_name='Сумма 2', null=True, blank=True)
    sum_3 = models.IntegerField(verbose_name='Сумма 3', null=True, blank=True)
    commission = models.FloatField(verbose_name='Комиссия за выдачу', default=0)
    commission_2 = models.FloatField(verbose_name='Комиссия за выдачу 2', null=True, blank=True)
    commission_3 = models.FloatField(verbose_name='Комиссия за выдачу 3', null=True, blank=True)
    commission_cash = models.FloatField(verbose_name='Коммиссия за обналичивание', default=0)

    def __str__(self):
        return self.product_name


class Client(models.Model):
    nomer_zayavki = models.IntegerField(unique=True, default=next_number, verbose_name='Номер заявки')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата заявки')
    fio_klienta = models.CharField(max_length=100, verbose_name='ФИО клиента/Наименование компании')
    summa_zayavki = models.IntegerField(null=False, verbose_name='Сумма заявки')
    purpose = models.CharField(max_length=200, choices=PURPOSE_CHOICES, verbose_name='Цель кредита')
    srok_kredita = models.IntegerField(null=False, verbose_name='Срок кредита')
    product = models.ForeignKey(Product, on_delete=models.SET('Удаленный продукт'),
                                verbose_name='Наименование продукта')
    zalog = models.CharField(max_length=20, choices=ZALOG_CHOISES, verbose_name='Обеспечение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    istochnik = models.CharField(max_length=20, choices=ISTOCHNIK_CHOISES, verbose_name='Источник погашения')
    reason = models.CharField(max_length=200, null=True, blank=True, verbose_name='Причина отказа/Условия одобрения')
    date_refuse = models.DateTimeField(default=one_day_more, null=True, blank=True,
                                       verbose_name='Дата отказа/одобрения')
    protokol_number = models.CharField(max_length=20, unique=True, null=True, blank=True,
                                       verbose_name='Номер протокола')
    credit_user = models.ForeignKey(Officer, on_delete=models.SET('Удаленный пользователь'),
                                    verbose_name='Кредитный специалист')

    def __str__(self):
        return self.fio_klienta

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'pk': self.pk})

    def get_interest_rate(self):
        if self.product.interest_rate_2 is not None:
            if self.product.sum < self.summa_zayavki < self.product.sum_2:
                return self.product.interest_rate_2
            elif self.product.sum_2 <= self.summa_zayavki <= self.product.sum_3:
                return self.product.interest_rate_3
            else:
                return self.product.interest_rate
        else:
            return self.product.interest_rate

    def get_commission(self):
        if self.product.interest_rate == 0:
            if self.srok_kredita <= 6:
                return 2
            else:
                return 4
        else:
            if self.product.commission_2 is not None:
                if self.product.sum < self.summa_zayavki < self.product.sum_2:
                    return self.product.commission_2
                elif self.product.sum_2 < self.summa_zayavki < self.product.sum_3:
                    return self.product.commission_3
                else:
                    return self.product.commission
            else:
                return self.product.commission