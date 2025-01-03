from django.shortcuts import render, redirect
from django.db import connection
from .models import Cliente, Venda, Prato
 
def get_estatisticas():
    with connection.cursor() as cursor:
        cursor.callproc('estatisticas')
        stats = cursor.fetchall()
    return stats
 
def estatisticas_view(request):
    with connection.cursor() as cursor:
        cursor.callproc('estatisticas')
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'restaurante_app/estatisticas.html', context)

def total_revenue_by_dish_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.nome AS prato, SUM(v.valor) AS total_revenue
            FROM restaurante_app_venda v
            JOIN restaurante_app_prato p ON v.prato_id = p.id
            GROUP BY p.nome
            ORDER BY total_revenue DESC;
        """)
        results = cursor.fetchall()
    context = {
        'results': results,
    }
    return render(request, 'restaurante_app/total_de_receita_por_prato.html', context)

def monthly_sales_by_dish_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.nome AS prato, DATE_FORMAT(v.dia, '%Y-%m') AS mes, SUM(v.valor) AS total_sales
            FROM restaurante_app_venda v
            JOIN restaurante_app_prato p ON v.prato_id = p.id
            GROUP BY p.nome, mes
            ORDER BY p.nome, mes;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'restaurante_app/vendas_mensal_de_pratos.html', context)

def top_clients_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nome AS cliente, SUM(v.valor) AS total_spent
            FROM restaurante_app_venda v
            JOIN restaurante_app_cliente c ON v.cliente_id = c.id
            GROUP BY c.nome
            ORDER BY total_spent DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'restaurante_app/melhores_clientes.html', context)
