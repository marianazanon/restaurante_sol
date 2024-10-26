from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from restaurante_app.models import Cliente, Venda, Prato, Fornecedor, Usos, Ingredientes
from django.core.management import call_command
from django.db import connection
from decouple import config

class Command(BaseCommand):
    help = 'cria usuários, grupos e dados iniciais no banco'

    def handle(self, *args, **kwargs):
        gerente_password = config('GERENTE_PASSWORD')
        funcionario_password = config('FUNCIONARIO_PASSWORD')
        superuser_password = config('SUPERUSER_PASSWORD')

        gerente_group, _ = Group.objects.get_or_create(name='gerente')

        permissions = Permission.objects.filter(
            content_type__in=[
                ContentType.objects.get_for_model(Cliente),
                ContentType.objects.get_for_model(Prato),
                ContentType.objects.get_for_model(Fornecedor),
                ContentType.objects.get_for_model(Usos),
                ContentType.objects.get_for_model(Venda),
                ContentType.objects.get_for_model(Ingredientes),
            ]
        )
        gerente_group.permissions.set(permissions)

        funcionario_group, _ = Group.objects.get_or_create(name='funcionario')

        funcionario_group.permissions.set(
            Permission.objects.filter(
                codename__startswith='add'
            ) | Permission.objects.filter(
                codename__startswith='view'
            )
        )

        funcionario_group.permissions.remove(
            *Permission.objects.filter(codename__startswith='delete')
        )
        funcionario_group.permissions.remove(
            *Permission.objects.filter(codename__startswith='change')
        )

        print('Groupos e permissões criados com sucesso.')

        gerente_user = User.objects.create_user(
            username='gerente',
            password=gerente_password,
            email='gerente@sol.com'
        )
        gerente_user.groups.add(gerente_group)

        funcionario_user = User.objects.create_user(
            username='funcionario',
            password=funcionario_password,
            email='funcionario@sol.com'
        )
        funcionario_user.groups.add(funcionario_group)

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password=superuser_password,
                email='admin@sol.com'
            )

        gerente_user = User.objects.get(username='gerente')
        gerente_user.is_staff = True
        gerente_user.save()

        funcionario_user = User.objects.get(username='funcionario')
        funcionario_user.is_staff = True
        funcionario_user.save()

        self.stdout.write(self.style.SUCCESS('Usuários e grupos criados com sucesso!'))

        call_command('setup_triggers')
        call_command('setup_procedures')

        self.populate_initial_data()

    def populate_initial_data(self):
        sql_files = [
            'restaurante_app/sql/insert_clientes.sql',
            'restaurante_app/sql/insert_fornecedor.sql',
            'restaurante_app/sql/insert_ingredientes.sql',
            'restaurante_app/sql/insert_pratos.sql',
            'restaurante_app/sql/populate_usos.sql',
        ]
        
        with connection.cursor() as cursor:
            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    cursor.execute(sql)
        self.stdout.write(self.style.SUCCESS('Dados iniciais carregados com sucesso!'))
