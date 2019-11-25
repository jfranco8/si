
----------------------------
----- SET NETAMOUNT & TOTALAMOUNT
----------------------------
create or replace function setOrderAmount() returns void as $$ begin
  update public.orders
  set netamount = total, totalamount = total*(100+tax)/100
  from(select sum(price) as total, orderid
  from orderdetail group by orderid) as alias
  where alias.orderid = orders.orderid;
end;
$$
language plpgsql;
select * from setOrderAmount()
