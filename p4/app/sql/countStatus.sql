
---- Crear base de datos y cargar los datos justo antes
-- dropdb -U alumnodb si1
-- createdb -U alumnodb si1
-- cat dump_v1.1-P4.sql | psql -U alumnodb si1
-- cat countStatus.sql | psql -U alumnodb si1

-------------------------------------------------
----- Consulta 1 recién creada la base de datos
-------------------------------------------------
explain analyze
select count(*)
from orders
where status is null;

-------------------------------------------------
----- Consulta 2 recién creada la base de datos
-------------------------------------------------
explain analyze
select count(*)
from orders
where status ='Shipped';

-------------------------------------------------
----- Creación de un indice
-------------------------------------------------
create index i on orders(status);

-------------------------------------------------
----- Consulta 1 tras crear indice
-------------------------------------------------
explain analyze
select count(*)
from orders
where status is null;

-------------------------------------------------
----- Consulta 2 tras crear indice
-------------------------------------------------
explain analyze
select count(*)
from orders
where status ='Shipped';

-------------------------------------------------
----- Estadisticas tabla orders
-------------------------------------------------
analyze orders;

-------------------------------------------------
----- Consulta 1 tras generacion de estadisticas
-------------------------------------------------
explain analyze
select count(*)
from orders
where status is null;

-------------------------------------------------
----- Consulta 2 tras generacion de estadisticas
-------------------------------------------------
explain analyze
select count(*)
from orders
where status ='Shipped';

-------------------------------------------------
----- Consulta 3 tras generacion de estadisticas
-------------------------------------------------
explain analyze
select count(*)
from orders
where status ='Paid';

-------------------------------------------------
----- Consulta 4 tras generacion de estadisticas
-------------------------------------------------
explain analyze
select count(*)
from orders
where status ='Processed';
