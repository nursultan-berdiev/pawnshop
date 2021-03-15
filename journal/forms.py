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
                  'telephone_number',
                  'zalog',
                  'comment',)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['telephone_number'].widget.attrs.update({'type': 'tel'})


class EarlyRepaymentForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['itogo_k_vyplate']
