CREATE TRIGGER add_points_after_sale
AFTER INSERT ON restaurante_app_venda
FOR EACH ROW
BEGIN
    DECLARE points INT;

    SET points = FLOOR(NEW.valor / 10);

    UPDATE restaurante_app_cliente
    SET pontos = pontos + points
    WHERE id = NEW.cliente_id;
END;
