
----------------------------
----- SET PRICE ORDER
----------------------------
update public.orderdetail
set
  price = orderdetail.quantity * prod_mov.price /
  power (1.02, extract (year from now()) - extract (year from orders.orderdate))
from orders, (products NATURAL JOIN imdb_movies) AS prod_mov
where orders.orderid = orderdetail.orderid and prod_mov.prod_id=orderdetail.prod_id;
