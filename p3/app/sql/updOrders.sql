drop function if exists updOrders();
drop trigger if exists updOrders on orderdetail;
create or replace function updOrders() returns trigger as $$

begin
  if (TG_OP = 'INSERT') then
    update orders set netamount = netamount + new.price*new.quantity where orderid=new.orderid;
    update orders set totalamount = netamount*(100+tax)/100 where orderid=new.orderid;
    return null;
  elsif (TG_OP = 'UPDATE') then
  update orders set netamount = netamount + new.price*new.quantity - old.price*old.quantity where orderid=old.orderid;
  update orders set totalamount = netamount*(100+tax)/100 where orderid=old.orderid;
    return null;
  elsif (TG_OP = 'DELETE') then
    update orders set netamount = netamount - old.price*old.quantity where orderid=old.orderid;
    update orders set totalamount = netamount*(100+tax)/100 where orderid=old.orderid;
    return null;
  end if;
end;
$$
language plpgsql;

create trigger updOrders before INSERT or UPDATE or DELETE on orderdetail for each row execute procedure updOrders();
