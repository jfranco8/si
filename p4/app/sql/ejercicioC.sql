----------------------------
----- ALTERNATIVA 1
----------------------------
explain analyze
select customerid
from customers
where customerid not in
  (select customerid
  from orders
  where status='Paid'
);


----------------------------
----- ALTERNATIVA 2
----------------------------
explain analyze
select customerid
from (
  select customerid
  from customers
  union all
  select customerid
  from orders
  where status='Paid'
)as A
group by customerid
having count(*) =1;


----------------------------
----- ALTERNATIVA 3
----------------------------
explain analyze
select customerid
from customers except
  select customerid
  from orders
  where status='Paid';
