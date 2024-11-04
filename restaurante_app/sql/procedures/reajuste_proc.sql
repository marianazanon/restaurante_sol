CREATE PROCEDURE reajuste(IN pct_reajuste DECIMAL(5, 2))
BEGIN
    UPDATE restaurante_app_prato
    SET valor = valor + (valor * (pct_reajuste / 100));
END;
