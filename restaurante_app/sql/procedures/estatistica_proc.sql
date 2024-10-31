REATE PROCEDURE estatisticas()
BEGIN
    DECLARE most_sold_dish_id INT;
    DECLARE least_sold_dish_id INT;
    DECLARE most_sold_dish_name VARCHAR(100);
    DECLARE least_sold_dish_name VARCHAR(100);
    DECLARE revenue_most_sold_dish DECIMAL(10, 2);
    DECLARE revenue_least_sold_dish DECIMAL(10, 2);
    DECLARE highest_sales_month_most_sold_dish VARCHAR(7);
    DECLARE lowest_sales_month_most_sold_dish VARCHAR(7);
    DECLARE highest_sales_month_least_sold_dish VARCHAR(7);
    DECLARE lowest_sales_month_least_sold_dish VARCHAR(7);

    SELECT prato_id, SUM(valor) INTO most_sold_dish_id, revenue_most_sold_dish
    FROM restaurante_app_venda
    GROUP BY prato_id
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT prato_id, SUM(valor) INTO least_sold_dish_id, revenue_least_sold_dish
    FROM restaurante_app_venda
    GROUP BY prato_id
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT nome INTO most_sold_dish_name FROM restaurante_app_prato WHERE id = most_sold_dish_id;

    SELECT nome INTO least_sold_dish_name FROM restaurante_app_prato WHERE id = least_sold_dish_id;

    SELECT DATE_FORMAT(dia, '%Y-%m'), SUM(valor) INTO highest_sales_month_most_sold_dish, @max_sales
    FROM restaurante_app_venda
    WHERE prato_id = most_sold_dish_id
    GROUP BY DATE_FORMAT(dia, '%Y-%m')
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT DATE_FORMAT(dia, '%Y-%m'), SUM(valor) INTO lowest_sales_month_most_sold_dish, @min_sales
    FROM restaurante_app_venda
    WHERE prato_id = most_sold_dish_id
    GROUP BY DATE_FORMAT(dia, '%Y-%m')
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT DATE_FORMAT(dia, '%Y-%m'), SUM(valor) INTO highest_sales_month_least_sold_dish, @max_sales
    FROM restaurante_app_venda
    WHERE prato_id = least_sold_dish_id
    GROUP BY DATE_FORMAT(dia, '%Y-%m')
    ORDER BY SUM(valor) DESC
    LIMIT 1;

    SELECT DATE_FORMAT(dia, '%Y-%m'), SUM(valor) INTO lowest_sales_month_least_sold_dish, @min_sales
    FROM restaurante_app_venda
    WHERE prato_id = least_sold_dish_id
    GROUP BY DATE_FORMAT(dia, '%Y-%m')
    ORDER BY SUM(valor) ASC
    LIMIT 1;

    SELECT
        most_sold_dish_name AS PratoMaisVendido,
        least_sold_dish_name AS PratoMenosVendido,
        revenue_most_sold_dish AS ReceitaPratoMaisVendido,
        highest_sales_month_most_sold_dish AS MesMaiorVendaPratoMaisVendido,
        lowest_sales_month_most_sold_dish AS MesMenorVendaPratoMaisVendido,
        revenue_least_sold_dish AS ReceitaPratoMenosVendido,
        highest_sales_month_least_sold_dish AS MesMaiorVendaPratoMenosVendido,
        lowest_sales_month_least_sold_dish AS MesMenorVendaPratoMenosVendido;
END;