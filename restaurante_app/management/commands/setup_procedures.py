from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Criação dos procedures da database'

    def handle(self, *args, **kwargs):
        sql_files = [
            'restaurante_app/sql/procedures/estatistica_proc.sql',
            'restaurante_app/sql/procedures/gastar_pontos_proc.sql',
            'restaurante_app/sql/procedures/reajuste_proc.sql',
            'restaurante_app/sql/procedures/sorteio_proc.sql',
        ]

        with connection.cursor() as cursor:
            cursor.execute("DROP PROCEDURE IF EXISTS reajuste")
            cursor.execute("DROP PROCEDURE IF EXISTS sorteio")
            cursor.execute("DROP PROCEDURE IF EXISTS gastar_pontos")
            cursor.execute("DROP PROCEDURE IF EXISTS estatisticas")

            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    statements = sql.split('END;')
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement + 'END;')

        self.stdout.write(self.style.SUCCESS('Procedures criados com sucesso!'))