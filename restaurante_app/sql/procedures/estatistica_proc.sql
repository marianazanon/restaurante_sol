CREATE PROCEDURE estatisticas()
BEGIN
    DECLARE most_sold_id INT;
    DECLARE least_sold_id INT;

    SELECT prato_id, COUNT(prato_id) AS total_sales
    INTO most_sold_id
    FROM restaurante_app_venda
    GROUP BY prato_id
    ORDER BY total_sales DESC
    LIMIT 1;

    SELECT prato_id, COUNT(prato_id) AS total_sales
    INTO least_sold_id
    FROM restaurante_app_venda
    GROUP BY prato_id
    ORDER BY total_sales ASC
    LIMIT 1;

    SELECT cliente_id, COUNT(cliente_id)
    FROM restaurante_app_venda
    WHERE prato_id = most_sold_id
    GROUP BY cliente_id
    ORDER BY COUNT(cliente_id) DESC
    LIMIT 1;

    SELECT SUM(valor) FROM restaurante_app_venda WHERE prato_id = most_sold_id;

    SELECT MONTH(dia) AS month, COUNT(*) AS sales
    FROM restaurante_app_venda
    WHERE prato_id = most_sold_id
    GROUP BY month
    ORDER BY sales DESC
    LIMIT 1;
    
    SELECT MONTH(dia) AS month, COUNT(*) AS sales
    FROM restaurante_app_venda
    WHERE prato_id = most_sold_id
    GROUP BY month
    ORDER BY sales ASC
    LIMIT 1;

    SELECT SUM(valor) FROM restaurante_app_venda WHERE prato_id = least_sold_id;

    SELECT MONTH(dia) AS month, COUNT(*) AS sales
    FROM restaurante_app_venda
    WHERE prato_id = least_sold_id
    GROUP BY month
    ORDER BY sales DESC
    LIMIT 1;
    
    SELECT MONTH(dia) AS month, COUNT(*) AS sales
    FROM restaurante_app_venda
    WHERE prato_id = least_sold_id
    GROUP BY month
    ORDER BY sales ASC
    LIMIT 1;
END