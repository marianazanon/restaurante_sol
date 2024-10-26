CREATE PROCEDURE Gastar_pontos(IN cliente_id INT, IN prato_id INT)
BEGIN
    DECLARE prato_valor DECIMAL(10, 2);
    DECLARE cliente_pontos INT;
    DECLARE ponto_extra INT DEFAULT 0;
    DECLARE msg VARCHAR(255);

    SELECT valor INTO prato_valor FROM restaurante_app_prato WHERE id = prato_id;

    SELECT pontos INTO cliente_pontos FROM restaurante_app_cliente WHERE id = cliente_id;

    IF prato_valor != FLOOR(prato_valor) THEN
        SET ponto_extra = 1;
    END IF;

    IF cliente_pontos >= prato_valor THEN
        UPDATE restaurante_app_cliente
        SET pontos = pontos - (FLOOR(prato_valor) + ponto_extra)
        WHERE id = cliente_id;

    ELSE
        SET msg = CONCAT('Cliente não tem pontos suficientes para a compra.');
        INSERT INTO restaurante_app_eventlog_message (message, created_at)
        VALUES (msg, NOW());

        SIGNAL SQLSTATE '45000' 
    END IF;
END