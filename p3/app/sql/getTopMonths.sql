CREATE OR REPLACE FUNCTION getTopMonths(precio numeric, num_product integer)
RETURNS TABLE(
	anno double precision,
	mes double precision,
  total numeric,
	productos bigint) AS $topMonths$ BEGIN
RETURN QUERY(

  SELECT *
  FROM (
  	SELECT extract (year FROM orderdate) AS anno, extract (month FROM orderdate) AS mes, sum(totalamount) as total, sum(quantity) as productos
  	FROM orders JOIN orderdetail ON orders.orderid = orderdetail.orderid
  	GROUP BY anno, mes) AS T
  WHERE T.total >= precio OR T.productos >= num_product
  ORDER BY anno, mes

);
END;
$topMonths$ language plpgsql;
