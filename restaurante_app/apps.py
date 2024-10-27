from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class RestauranteAppConfig(AppConfig):
    name = 'restaurante_app'

    def ready(self):
        post_migrate.connect(create_users_and_groups, sender=self)

def create_users_and_groups(sender, **kwargs):
    try:
        call_command('create_users_and_groups')
        print("Usuários e grupos criados com sucesso após a migração.")
    except Exception as e:
        print(f"Erro ao criar usuários e grupos após a migração: {e}")
