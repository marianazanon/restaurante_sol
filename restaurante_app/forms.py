from django import forms
from django.db import connection, OperationalError, transaction
from .models import Venda, Reajuste, Sorteio, Prato

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['prato', 'cliente', 'quantidade']
        
    def clean(self):
        cleaned_data = super().clean()
        prato = cleaned_data.get('prato')
        if prato and not prato.disponivel:
            raise forms.ValidationError('Compra não permitida: Prato indisponível.')
        return cleaned_data

    def save(self, commit=True):
        try:
            with transaction.atomic():
                return super().save(commit=commit)
        except OperationalError as e:
            transaction.set_rollback(True)
            error_code = e.args[0]
            error_message = e.args[1]
            if error_code == 1644:
                self.add_error(None, error_message)
                raise forms.ValidationError(error_message)
            else:
                self.add_error(None, f"Erro ao salvar a venda: {error_message}")
                raise forms.ValidationError(f"Erro ao salvar a venda: {error_message}")

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
