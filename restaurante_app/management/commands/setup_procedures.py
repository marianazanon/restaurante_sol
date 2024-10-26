from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Criação dos procedures da database'

    def handle(self, *args, **kwargs):
        sql_files = [

        ]

        with connection.cursor() as cursor:


            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    statements = sql.split('END;')
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement + 'END;')

        self.stdout.write(self.style.SUCCESS('Procedures criados com sucesso!'))