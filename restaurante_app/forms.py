from django import forms
from django.db import connection
from .models import Venda, Reajuste, Sorteio, Prato

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['prato', 'cliente', 'quantidade']

class ReajusteForm(forms.ModelForm):
    prato = forms.ModelChoiceField(queryset=Prato.objects.all(), empty_label="Selecione um prato")

    class Meta:
        model = Reajuste
        fields = ['pct_reajuste', 'prato']

    def save(self, commit=True):
        pct_reajuste = self.cleaned_data.get('pct_reajuste')
        prato = self.cleaned_data.get('prato')

        with connection.cursor() as cursor:
            cursor.callproc('reajuste', [pct_reajuste])

        return super().save(commit=commit)

class SorteioForm(forms.ModelForm):
    class Meta:
        model = Sorteio
        fields = []

    def save(self, commit=True):
        with connection.cursor() as cursor:
            cursor.callproc('sorteio')

        return super().save(commit=commit)
