from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Criação dos triggers da database'

    def handle(self, *args, **kwargs):
        sql_files = [
            'restaurante_app/sql/triggers/add_points_after_sale.sql',
            'restaurante_app/sql/triggers/make_dish_unavailable_expires.sql',
            'restaurante_app/sql/triggers/prevent_unavailable_dish_purchase.sql',
            'restaurante_app/sql/triggers/reduce_ingredient_quantity.sql',
        ]

        with connection.cursor() as cursor:

            for sql_file in sql_files:
                with open(sql_file, 'r') as file:
                    sql = file.read()
                    statements = sql.split('END;')
                    for statement in statements:
                        if statement.strip():
                            cursor.execute(statement + 'END;')

        self.stdout.write(self.style.SUCCESS('Triggers ativados com sucesso!'))