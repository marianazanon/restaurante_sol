CREATE TRIGGER prevent_unavailable_prato_purchase
BEFORE INSERT ON restaurante_app_venda
FOR EACH ROW
BEGIN
    DECLARE prato_status BOOLEAN;
    DECLARE msg VARCHAR(255);

    SET prato_status = (SELECT disponivel FROM restaurante_app_prato WHERE id = NEW.prato_id);

    IF prato_status = FALSE THEN
        SET msg = 'Compra não permitida: Prato indisponível.';

        INSERT INTO restaurante_app_eventlog_message (message, created_at)
        VALUES (msg, NOW());

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = msg;
    END IF;
END;
