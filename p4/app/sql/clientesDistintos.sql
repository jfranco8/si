drop
  index if exists idx_orderdate;
drop
  index if exists idx_totalamount;

-- sin indices
explain
SELECT
  count(DISTINCT customerid)
FROM
  orders
WHERE
  totalamount > 100
  and TO_CHAR(orderdate, 'YYYYMM') = '201504';


  drop
    index if exists idx_orderdate;
  drop
    index if exists idx_totalamount;
-- Indice en columna orderdate
create index idx_orderdate ON orders (orderdate);
drop index idx_totalamount;
explain
SELECT
  count(DISTINCT customerid)
FROM
  orders
WHERE
  totalamount > 100
  and TO_CHAR(orderdate, 'YYYYMM') = '201504';


drop
  index if exists idx_orderdate;
drop
  index if exists idx_totalamount;
-- Indice en columna totalamount
drop index idx_orderdate;
create index idx_totalamount ON orders (totalamount);
explain
SELECT
  count(DISTINCT customerid)
FROM
  orders
WHERE
  totalamount > 100
  and TO_CHAR(orderdate, 'YYYYMM') = '201504';

drop
  index if exists idx_orderdate;
drop
  index if exists idx_totalamount;
-- Indice en las dos columnas
create index idx_orderdate ON orders (orderdate);
create index idx_totalamount ON orders (totalamount);
explain
SELECT
  count(DISTINCT customerid)
FROM
  orders
WHERE
  totalamount > 100
  and TO_CHAR(orderdate, 'YYYYMM') = '201504';
