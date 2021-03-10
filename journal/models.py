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

TRANSACTION_CHOICES = (
    ('Приход', 'Приход'),
    ('Расход', 'Расход'),
)


def one_day_more():
    return timezone.now() + timezone.timedelta(days=1)


def next_number():
    if Product.objects.all().count() == 0:
        return 1
    else:
        last_loan = Product.objects.order_by('-nomer_bileta')[0]
        number = last_loan.nomer_bileta
        return int(number + 1)


class Zalog_types(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип залога')

    def __str__(self):
        return self.type


class Product(models.Model):
    date_posted = models.DateField(default=timezone.now, verbose_name='Дата заявки')
    nomer_bileta = models.IntegerField(unique=True, default=next_number, verbose_name='Номер билета')
    fio_klienta = models.CharField(max_length=50, verbose_name='ФИО клиента')
    summa_zayavki = models.IntegerField(null=False, verbose_name='Сумма заявки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус',
                              default=STATUS_CHOICES[0][0])
    stavka_day = models.FloatField(null=False, default=int(1), verbose_name='Процентная ставка в день')
    srok_kredita = models.IntegerField(null=False, verbose_name='Срок займа в днях')
    comment = models.TextField(null=True, blank=True, verbose_name='Дополнительные комментарии')
    credit_user = models.ForeignKey(Officer, on_delete=models.SET('Удаленный пользователь'),
                                    verbose_name='Кредитный специалист')
    ostatok = models.FloatField(null=True, blank=True, verbose_name='Остаток основной суммы')
    stavka_period = models.FloatField(null=True, verbose_name='Ожидаемый доход за период')
    expected_stavka_day = models.FloatField(null=True, verbose_name='Ожидаемый доход в день')
    fact_day = models.FloatField(null=True, blank=True, verbose_name='Начисленные проценты')
    itogo_k_vyplate = models.FloatField(null=True, blank=True, verbose_name='Итого к выплате')
    fact_loan_day = models.IntegerField(null=False, blank=True, verbose_name='Количество фактических дней')
    date_plan_pay = models.DateField(null=False, blank=False, verbose_name='Дата окончания')
    date_fact_pay = models.DateField(null=True, blank=True, verbose_name='Дата фактического окончания')
    zalog = models.TextField(verbose_name='Наименование залога')

    def __str__(self):
        return str(self.nomer_bileta)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.stavka_period > self.fact_day:
            self.itogo_k_vyplate = self.ostatok + self.stavka_period
        elif self.stavka_period < self.fact_day:
            self.itogo_k_vyplate = self.ostatok + self.fact_day
        else: self.itogo_k_vyplate = self.ostatok + self.fact_day
        self.expected_stavka_day = self.ostatok * self.stavka_day / 100
        if self.fact_day > self.stavka_period:
            self.status = 'Просрочен'
        super(Product, self).save(*args, **kwargs)


class PrihodRashod(models.Model):
    summa = models.FloatField(verbose_name='Сумма транзакции')
    type = models.CharField(max_length=20, verbose_name='Тип транзакции', choices=TRANSACTION_CHOICES)
    date = models.DateField(verbose_name='Дата транзакции')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Займ')
    comment = models.CharField(max_length=200, verbose_name='Комментарий')

    def __str__(self):
        return '{} --- {}'.format(self.type, self.comment)


class WorkDays(models.Model):
    day = models.DateField(verbose_name='Дата')
    is_calculated = models.BooleanField(verbose_name='Начисление')
    calc_sum = models.FloatField(verbose_name='Сумма начислений')

    def __str__(self):
        return 'На дату {} начислено {} сом'.format(self.day, self.calc_sum)