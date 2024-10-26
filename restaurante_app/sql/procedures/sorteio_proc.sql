CREATE PROCEDURE sorteio()
BEGIN
    DECLARE random_cliente_id INT;
    
    SELECT id INTO random_cliente_id
    FROM restaurante_app_cliente
    ORDER BY RAND()
    LIMIT 1;

    UPDATE restaurante_app_cliente
    SET pontos = pontos + 100
    WHERE id = random_cliente_id;

    SELECT nome FROM restaurante_app_cliente WHERE id = random_cliente_id;
END
