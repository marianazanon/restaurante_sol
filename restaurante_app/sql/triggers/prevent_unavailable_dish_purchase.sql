CREATE TRIGGER prevent_unavailable_prato_purchase
BEFORE INSERT ON restaurante_app_venda
FOR EACH ROW
BEGIN
    DECLARE prato_status BOOLEAN;

    SELECT disponivel INTO prato_status 
    FROM restaurante_app_prato 
    WHERE id = NEW.prato_id;

    IF prato_status = FALSE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Compra não permitida: Prato indisponível.';
    END IF;
END
