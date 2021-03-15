from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('nomer_bileta',
                  'fio_klienta',
                  'summa_zayavki',
                  'stavka_day',
                  'srok_kredita',
                  'date_posted',
                  'zalog',
                  'comment',)


class EarlyRepaymentForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['itogo_k_vyplate']
