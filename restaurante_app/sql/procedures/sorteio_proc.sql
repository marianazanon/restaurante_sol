CREATE PROCEDURE sorteio()
BEGIN
    DECLARE random_cliente_id INT;
    DECLARE client_name VARCHAR(100);
    DECLARE current_points INT;
    DECLARE log_message VARCHAR(255);

    SELECT id INTO random_cliente_id
    FROM restaurante_app_cliente
    ORDER BY RAND()
    LIMIT 1;

    UPDATE restaurante_app_cliente
    SET pontos = pontos + 100
    WHERE id = random_cliente_id;

    SELECT nome, pontos INTO client_name, current_points
    FROM restaurante_app_cliente
    WHERE id = random_cliente_id;

    SET log_message = CONCAT('Cliente ', client_name, ' recebeu 100 pontos no sorteio. Pontuação atual: ', current_points);
    INSERT INTO restaurante_app_eventlog_message (message, created_at)
    VALUES (log_message, NOW());

    SELECT client_name AS Nome, current_points AS Pontos;
END;