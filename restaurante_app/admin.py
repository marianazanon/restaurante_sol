from django.contrib import admin, messages
from django import forms
from django.db import connection
from django.urls import path
from django.http import HttpRequest
from .models import Cliente, Prato, Venda, Fornecedor, Usos, Ingredientes, Reajuste, Sorteio, EventLog_Message
from .views import estatisticas_view, total_revenue_by_dish_view, monthly_sales_by_dish_view, top_clients_view
from .forms import ReajusteForm, SorteioForm

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
    list_display = ('nome', 'idade', 'sexo', 'nascimento', 'pontos')
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
    search_fields = ('cliente__nome', 'prato__nome')
    exclude = ('valor',)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='funcionario').exists():
            return False
        return super().has_change_permission(request, obj)

class ReajusteAdmin(admin.ModelAdmin):
    form = ReajusteForm
    list_display = ['pct_reajuste', 'prato']

    def save_model(self, request, obj, form, change):
        pct_reajuste = form.cleaned_data.get('pct_reajuste')
        with connection.cursor() as cursor:
            cursor.callproc('reajuste', [pct_reajuste])

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
            cursor.callproc('sorteio')

        latest_log = EventLog_Message.objects.order_by('-created_at').first()
        
        if latest_log:
            messages.success(request, latest_log.message)
        else:
            messages.info(request, "No log message available for this sorteio.")

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

class CustomAdminSite(admin.AdminSite):
    site_header = "Administração Restaurante Sol"
   
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('total-revenue-by-supplier/', monthly_sales_by_dish_view, name='vendas_mensal_de_pratos'),
            path('total-revenue-by-dish/', total_revenue_by_dish_view, name='total_de_receita_por_prato'),
            path('top-clients/', top_clients_view, name='melhores_clientes'),
            path('estatisticas/', estatisticas_view, name='estatisticas'),
        ]
        return my_urls + urls

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Prato, PratoAdmin)
admin_site.register(Venda, VendaAdmin)
admin_site.register(Fornecedor)
admin_site.register(Usos)
admin_site.register(Ingredientes)
admin_site.register(Reajuste, ReajusteAdmin)
admin_site.register(Sorteio, SorteioAdmin)
