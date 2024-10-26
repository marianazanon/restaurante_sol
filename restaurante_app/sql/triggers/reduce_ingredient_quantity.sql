CREATE TRIGGER reduce_ingredient_quantity_after_sale
AFTER INSERT ON restaurante_app_venda
FOR EACH ROW
BEGIN
    DECLARE qtd_needed INT;
    
    UPDATE restaurante_app_ingredientes AS ing
    JOIN restaurante_app_usos AS uso ON uso.ingrediente_id = ing.id
    SET ing.quantidade = ing.quantidade - 1
    WHERE uso.prato_id = NEW.prato_id;
END