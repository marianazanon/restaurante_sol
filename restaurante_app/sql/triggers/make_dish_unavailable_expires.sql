CREATE TRIGGER make_dish_unavaiable_expires
AFTER UPDATE ON restaurante_app_ingredientes
FOR EACH ROW
BEGIN
    IF NEW.data_validade < CURDATE() THEN

        UPDATE restaurante_app_prato
        SET disponivel = FALSE
        WHERE id IN (
            SELECT prato_id
            FROM restaurante_app_usos
            WHERE ingrediente_id = NEW.id
        );
    END IF;
END;
