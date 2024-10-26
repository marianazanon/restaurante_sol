from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class VendasAppConfig(AppConfig):
    name = 'restaurante_app'

    def ready(self):
        post_migrate.connect(create_users_and_groups, sender=self)

def create_users_and_groups(sender, **kwargs):
    call_command('create_users_and_groups')
