from django import forms
from .models import Venda, Reajuste, Sorteio

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['prato', 'cliente', 'quantidade']

class ReajusteForm(forms.ModelForm):
    class Meta:
        model = Reajuste
        fields = ['pct_reajuste', 'cargo']

    def save(self, commit=True):
        pct_reajuste = self.cleaned_data.get('pct_reajuste')
        cargo = self.cleaned_data.get('cargo')

        with connection.cursor() as cursor:
            cursor.callproc('Reajuste', [pct_reajuste])

        return super().save(commit=commit)

class SorteioForm(forms.ModelForm):
    class Meta:
        model = Sorteio
        fields = []

    def save(self, commit=True):
        with connection.cursor() as cursor:
            cursor.callproc('Sorteio')

        return super().save(commit=commit)
