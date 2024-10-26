from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Deleta todas as tabelas no banco de dados'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("SHOW TABLES;")
            for table in cursor.fetchall():
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        self.stdout.write(self.style.SUCCESS('Banco de dados deletado com sucesso!'))