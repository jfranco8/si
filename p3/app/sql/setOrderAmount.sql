
----------------------------
----- SET NETAMOUNT & TOTALAMOUNT
----------------------------
update public.orders
set netamount = total, totalamount = netamount*(100+tax)/100
from(select sum(price) as total, orderid
from orderdetail group by orderid) as alias
where alias.orderid = orders.orderid
