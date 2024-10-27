from django.shortcuts import render, redirect
from django.db import connection
from .models import Cliente, Venda, Prato
 
def get_estatisticas():
    with connection.cursor() as cursor:
        cursor.callproc('estatisticas')
        stats = cursor.fetchall()
    return stats
 
def estatisticas_view(request):
    stats = get_estatisticas()

    context = {
        'most_sold_dish': stats[0][0],
        'most_sold_dish_revenue': stats[1][0],
        'most_sold_dish_best_month': stats[2][0],
        'most_sold_dish_worst_month': stats[3][0],
        'least_sold_dish': stats[4][0],
        'least_sold_dish_revenue': stats[5][0],
        'least_sold_dish_best_month': stats[6][0],
        'least_sold_dish_worst_month': stats[7][0],
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

def total_revenue_by_supplier_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT f.nome AS fornecedor, SUM(v.valor) AS total_revenue
            FROM restaurante_app_venda v
            JOIN restaurante_app_prato p ON v.prato_id = p.id
            JOIN restaurante_app_fornecedor f ON p.fornecedor_id = f.id
            GROUP BY f.nome
            ORDER BY total_revenue DESC;
        """)
        results = cursor.fetchall()
    
    context = {
        'results': results,
    }
    return render(request, 'restaurante_app/total_de_receita_por_fornecedor.html', context)

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
