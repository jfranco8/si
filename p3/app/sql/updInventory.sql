drop function if exists updInventory();
drop trigger if exists updInventory on orders;
create or replace function updInventory() returns trigger as $$
declare temporal record;
begin
  if (new.status = 'Paid') then
    for temporal in select orderdetail.quantity, inventory.sales, inventory.stock, inventory.prod_id
                    from orderdetail, inventory
                    where inventory.prod_id=orderdetail.prod_id and orderid=new.orderid
    loop
      update inventory set sales = sales + temporal.quantity where temporal.prod_id = inventory.prod_id;
      update inventory set stock = stock - temporal.quantity where temporal.prod_id = inventory.prod_id;
      if ((temporal.stock - temporal.quantity) = 0) then
        insert into alerta(prod_id) values(temporal.prod_id);
      end if;
    end loop;
  end if;
  return null;
end;
$$
language plpgsql;

create trigger updInventory after UPDATE on orders for each row execute procedure updInventory();
