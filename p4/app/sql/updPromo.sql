ALTER TABLE customers ADD promo INTEGER;

DROP FUNCTION IF EXISTS promo();
CREATE FUNCTION promo() returns TRIGGER AS $$
BEGIN
	IF(TG_OP = 'INSERT') THEN
		UPDATE orders
		SET netamount = netamount*(100 - NEW.promo)/100
		WHERE customerid = NEW.customerid AND status IS NULL;
	ELSE
		UPDATE orders
		SET netamount = netamount*100/(100 - OLD.promo)
		WHERE customerid = NEW.customerid AND status IS NULL;
		UPDATE orders
		SET netamount = netamount*(100 - NEW.promo)/100
		WHERE customerid = NEW.customerid AND status IS NULL;
	END IF;
	PERFORM pg_sleep(30);
END;
$$ language plpgsql;
