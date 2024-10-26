from django.contrib import admin
from django import forms
from django.db import connection
from django.urls import path
from django.http import HttpRequest
from .models import Cliente, Prato, Venda, Fornecedor, Usos, Ingredientes
from .views import total_revenue_by_vendor_view, monthly_sales_by_product_view, top_clients_view, estatisticas_view
from .forms import ReajusteForm, SorteioForm  # Placeholder forms for models that don't exist yet
 
class PratoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'descricao', 'disponivel')
    search_fields = ('nome',)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)
   
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'sexo', 'nascimento')
    search_fields = ('nome',)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)
 
 
class VendaAdmin(admin.ModelAdmin):
    list_display = ('prato', 'cliente', 'quantidade', 'valor', 'dia', 'hora')
    search_fields = ('cliente_nome', 'prato_nome')
    exclude = ('valor',)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)

# Placeholder class for Reajuste model (not implemented yet)
class ReajusteAdmin(admin.ModelAdmin):
    form = ReajusteForm
    list_display = ['pct_reajuste', 'cargo']

    def save_model(self, request, obj, form, change):
        pct_reajuste = form.cleaned_data.get('pct_reajuste')
        cargo = form.cleaned_data.get('cargo')

        with connection.cursor() as cursor:
            cursor.callproc('Reajuste', [pct_reajuste, cargo])

        obj.pk = None
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return {
                'add': self.has_add_permission(request),
            }
        return {}

class SorteioAdmin(admin.ModelAdmin):
    form = SorteioForm

    def save_model(self, request, obj, form, change):
        with connection.cursor() as cursor:
            cursor.callproc('Sorteio')

        obj.pk = None
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return {
                'add': self.has_add_permission(request),
            }
        return {}
 