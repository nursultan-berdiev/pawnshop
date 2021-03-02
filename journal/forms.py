from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('nomer_bileta',
                  'fio_klienta',
                  'summa_zayavki',
                  'status',
                  'stavka_day',
                  'srok_kredita',
                  'date_posted',
                  'zalog',
                  'comment',
                  'credit_user',)
