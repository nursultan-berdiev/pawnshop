import xlsxwriter
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import name_user
from .models import Client, Product
from django.shortcuts import render, get_object_or_404
from openpyxl import *
from openpyxl.writer.excel import save_virtual_workbook
from transliterate import translit, get_available_language_codes
from datetime import datetime, timedelta


def is_valid_queryparam(param):
    return param != '' and param is not None


def base_list(request):
    query = Product.objects.all()
    context = {
        'query': query
    }
    return context


class ClientListView(ListView):
    model = Client
    template_name = 'journal/journal.html'
    context_object_name = 'clients'
    ordering = ['-nomer_zayavki']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['title'] = 'Журнал Кредитного Специалиста'
        context['products'] = Product.objects.all()
        return context


class ActiveListView(ListView):
    queryset = Client.objects.filter(status = 'На рассмотрении')
    template_name = 'journal/home.html'
    context_object_name = 'clients'
    ordering = ['-nomer_zayavki']
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(ActiveListView, self).get_context_data(**kwargs)
        context['title'] = 'Активные заявки'
        context['products'] = Product.objects.all()
        return context


def SearchFilterView(request):
    query_set = Client.objects.all()
    products = Product.objects.all()
    search_contains_query = request.GET.get('search_contains')
    search_exact_query = request.GET.get('search_exact')
    sum_Count_Min = request.GET.get('sum_Count_Min')
    sum_Count_Max = request.GET.get('sum_Count_Max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    product = request.GET.get('product')
    title = 'Результаты поиска'

    if is_valid_queryparam(search_contains_query):
        query_set = query_set.filter(fio_klienta__icontains=search_contains_query.title())

    if is_valid_queryparam(search_exact_query):
        query_set = query_set.filter(nomer_zayavki__iexact=search_exact_query)

    if is_valid_queryparam(sum_Count_Min):
        query_set = query_set.filter(summa_zayavki__gte=sum_Count_Min)

    if is_valid_queryparam(sum_Count_Max):
        query_set = query_set.filter(summa_zayavki__lt=sum_Count_Max)

    if is_valid_queryparam(date_min):
        query_set = query_set.filter(date_posted__gte=date_min)

    if is_valid_queryparam(date_max):
        query_set = query_set.filter(date_posted__lt=date_max)

    if is_valid_queryparam(product) and product != 'Выберите продукт...':
        query_set = query_set.filter(product__product_name=product)

    qs = query_set.values_list('id', flat=True)
    excel_list = []
    for i in qs:
        excel_list.append(i)

    request.session['excel_list'] = excel_list
    context = {
        'queryset': query_set,
        'products': products,
        'title': title,
    }

    return render(request, 'journal/search_form.html', context)


class ClientDetailView(DetailView):
    model = Client

    def test(self):
        user = self.get_object().credit_user
        username = name_user(user)  # Данный метод описан в файле users\models.py

        if self.request.user == username:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Подробно'
        context['products'] = Product.objects.all()
        return context


def excel_report(request, pk):
    client = get_object_or_404(Client, pk=pk)
    file = 'D:/Python/changan_journal/keylist.xlsx'

    key_book = load_workbook(file)
    worksheet = key_book['list']
    worksheet_graphic = key_book['graphic']

    customer_name = worksheet.cell(8, 5)
    customer_name.value = client.fio_klienta

    officer_name = worksheet.cell(10, 5)
    officer_name.value = client.credit_user.name

    date_pay = [1, 5, 10, 15, 20, 25]
    day = int(client.date_posted.strftime('%d'))
    if day not in date_pay:
        pay_day = min(date_pay, key=lambda x: abs(x - day))
        delta = pay_day - day
        count_date = client.date_posted + timedelta(days=delta)
    else:
        count_date = client.date_posted

    date_count = worksheet_graphic.cell(7, 3)
    date_count.value = count_date

    date = worksheet_graphic.cell(4, 4)
    date.value = client.date_posted

    commission = worksheet.cell(24, 5)
    comm = client.get_commission() / 100
    commission.value = comm

    obnal = worksheet.cell(25, 5)
    ob = client.product.commission_cash / 100
    obnal.value = ob

    zalog = worksheet.cell(35, 5)
    zalog.value = client.zalog

    sum = worksheet_graphic.cell(1, 4)
    sum.value = client.summa_zayavki

    stavka = worksheet_graphic.cell(2, 4)
    stavka.value = client.get_interest_rate()

    srok = worksheet_graphic.cell(3, 4)
    srok.value = client.srok_kredita

    key_book.save(file)

    def splitpart(value):
        if len(value.split()) == 3:
            return f'{value.split()[0]}{value.split()[1][0]}.{value.split()[2][0]}.'
        elif len(value.split()) == 2:
            return f'{value.split()[0]}{value.split()[1][0]}.'
        else:
            return f'{value.split()[0]}'

    file_name = splitpart(client.fio_klienta)
    file_name = translit(file_name, "ru", reversed=True)

    response = HttpResponse(save_virtual_workbook(key_book), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)

    return response


class ClientCreateView(CreateView):
    model = Client
    fields = ['nomer_zayavki',
              'fio_klienta',
              'summa_zayavki',
              'purpose',
              'srok_kredita',
              'product',
              'zalog',
              'status',
              'istochnik',
              'reason',
              'date_refuse',
              'protokol_number',
              'credit_user']

    def get_context_data(self, *args, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание заявки'
        context['products'] = Product.objects.all()
        return context


class ClientUpdateView(UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['fio_klienta',
              'summa_zayavki',
              'purpose',
              'srok_kredita',
              'product',
              'zalog',
              'status',
              'istochnik',
              'reason',
              'date_refuse',
              'protokol_number',
              'credit_user']

    def get_context_data(self, *args, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Измнение заявки'
        context['products'] = Product.objects.all()
        return context

    def test_func(self):
        user = self.get_object().credit_user
        username = name_user(user)

        if self.request.user == username:
            return True
        return False


class ClientDeleteView(UserPassesTestMixin, DeleteView):
    model = Client
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(ClientDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление заявки'
        context['products'] = Product.objects.all()
        return context

    def test_func(self):
        user = self.get_object().credit_user
        username = name_user(user)  # Данный метод описан в файле users\models.py

        if self.request.user == username:
            return True
        return False


def my_view(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=UKJournal.xlsx"
    context = {
        'in_memory': True,
        'remove_timezone': True
    }
    background = '#ebfcff'
    border = 1

    def add_custom_format(format):
        format.set_bg_color(background)
        format.set_border(border)
        format.set_bold()

        return format

    book = xlsxwriter.Workbook(response, context)
    sheet = book.add_worksheet('Журнал Кредитного Эксперта')
    sheet.set_column(0, 0, 6)
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 35)
    sheet.set_column(3, 3, 13)
    sheet.set_column(4, 4, 16)
    sheet.set_column(5, 5, 12)
    sheet.set_column(6, 6, 22)
    sheet.set_column(7, 7, 16)
    sheet.set_column(8, 8, 16)
    sheet.set_column(9, 9, 19)
    sheet.set_column(10, 10, 30)
    sheet.set_column(11, 11, 20)
    sheet.set_column(12, 12, 16)
    sheet.set_column(13, 13, 20)
    sheet.set_zoom(80)

    number_format = book.add_format({'num_format': '№#####0'})
    add_custom_format(number_format)

    month_format = book.add_format({'num_format': '##0 мес'})
    add_custom_format(month_format)

    money_format = book.add_format({'num_format': '#,###,##0 сом'})
    add_custom_format(money_format)

    date_format = book.add_format({'num_format': 'dd.mm.yyyy'})
    add_custom_format(date_format)

    style_format = book.add_format()
    add_custom_format(style_format)

    col = 0
    row = 0
    sheet.write(0, col, Client._meta.get_field("nomer_zayavki").verbose_name, style_format)
    sheet.write(row, col + 1, Client._meta.get_field("date_posted").verbose_name, style_format)
    sheet.write(row, col + 2, Client._meta.get_field("fio_klienta").verbose_name, style_format)
    sheet.write(row, col + 3, Client._meta.get_field("summa_zayavki").verbose_name, style_format)
    sheet.write(row, col + 4, Client._meta.get_field("purpose").verbose_name, style_format)
    sheet.write(row, col + 5, Client._meta.get_field("srok_kredita").verbose_name, style_format)
    sheet.write(row, col + 6, Client._meta.get_field("product").verbose_name, style_format)
    sheet.write(row, col + 7, Client._meta.get_field("zalog").verbose_name, style_format)
    sheet.write(row, col + 8, Client._meta.get_field("status").verbose_name, style_format)
    sheet.write(row, col + 9, Client._meta.get_field("istochnik").verbose_name, style_format)
    sheet.write(row, col + 10, Client._meta.get_field("reason").verbose_name, style_format)
    sheet.write(row, col + 11, Client._meta.get_field("date_refuse").verbose_name, style_format)
    sheet.write(row, col + 12, Client._meta.get_field("protokol_number").verbose_name, style_format)
    sheet.write(row, col + 13, Client._meta.get_field("credit_user").verbose_name, style_format)
    row = 1
    col = 0
    excel_list = request.session['excel_list']
    for a in excel_list:
        queryset = Client.objects.get(id=int(a))
        sheet.write(row, col, queryset.nomer_zayavki, number_format)
        sheet.write(row, col + 1, queryset.date_posted, date_format)
        sheet.write(row, col + 2, queryset.fio_klienta, style_format)
        sheet.write(row, col + 3, queryset.summa_zayavki, money_format)
        sheet.write(row, col + 4, queryset.purpose, style_format)
        sheet.write(row, col + 5, queryset.srok_kredita, month_format)
        sheet.write(row, col + 6, queryset.product.product_name, style_format)
        sheet.write(row, col + 7, queryset.zalog, style_format)
        sheet.write(row, col + 8, queryset.status, style_format)
        sheet.write(row, col + 9, queryset.istochnik, style_format)
        sheet.write(row, col + 10, queryset.reason, style_format)
        sheet.write(row, col + 11, queryset.date_refuse, date_format)
        sheet.write(row, col + 12, queryset.protokol_number, style_format)
        sheet.write(row, col + 13, queryset.credit_user.name, style_format)
        row = row + 1
    book.close()

    return response
