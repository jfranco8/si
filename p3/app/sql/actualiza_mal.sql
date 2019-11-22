-- --------------------
-- BORRAR DB ANTERIOR
-- --------------------

DROP TABLE
  ACTOR,
  ACTOR_PELICULA,
  PELICULA,
  DIRECTOR,
  DIRECTOR_PELICULA,
  GENERO_PELICULA,
  IDIOMA_PELICULA,
  PAIS_PELICULA,
  PRODUCTO,
  PRODUCTO_PELICULA,
  PEDIDO,
  PEDIDO_PRODUCTO,
  CLIENTE;

-- --------------------
-- TABLA ACTOR
-- --------------------

CREATE TABLE ACTOR (
  actorID integer PRIMARY KEY NOT NULL,
  nombre char(70)
);

ALTER TABLE ACTOR OWNER TO alumnodb;

CREATE SEQUENCE ACTOR_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ACTOR_SEQ OWNER TO alumnodb;

ALTER SEQUENCE ACTOR_SEQ OWNED BY ACTOR.actorID;

-- --------------------
-- RELACION ACTOR - PELICULA
-- --------------------

CREATE TABLE ACTOR_PELICULA (
  actorID integer NOT NULL,
  peliculaID integer NOT NULL,
  personaje char(500)
);

ALTER TABLE ACTOR_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PELICULA
-- --------------------

CREATE TABLE PELICULA (
  peliculaID integer PRIMARY KEY NOT NULL,
  titulo char(100),
  puntuacion integer,
  anno char(50),
  sinopsis char(500)
);

ALTER TABLE PELICULA OWNER TO alumnodb;

CREATE SEQUENCE PELICULA_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE PELICULA_SEQ OWNER TO alumnodb;

ALTER SEQUENCE PELICULA_SEQ OWNED BY PELICULA.peliculaID;

-- --------------------
-- TABLA DIRECTOR
-- --------------------

CREATE TABLE DIRECTOR (
  directorID integer PRIMARY KEY NOT NULL,
  nombre char(500)
);

ALTER TABLE DIRECTOR OWNER TO alumnodb;

CREATE SEQUENCE DIRECTOR_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE DIRECTOR_SEQ OWNER TO alumnodb;

ALTER SEQUENCE DIRECTOR_SEQ OWNED BY DIRECTOR.directorID;

-- --------------------
-- RELACION DIRECTOR - PELICULA
-- --------------------

CREATE TABLE DIRECTOR_PELICULA (
  directorID integer NOT NULL,
  peliculaID integer NOT NULL
);

ALTER TABLE DIRECTOR_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION GENERO - PELICULA
-- --------------------

CREATE TABLE GENERO_PELICULA (
  genero char(500),
  peliculaID integer
);

ALTER TABLE GENERO_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION IDIOMA - PELICULA
-- --------------------

CREATE TABLE IDIOMA_PELICULA (
  idioma char(500),
  peliculaID integer
);

ALTER TABLE IDIOMA_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION PAIS - PELICULA
-- --------------------

CREATE TABLE PAIS_PELICULA (
  pais char(500),
  peliculaID integer
);

ALTER TABLE PAIS_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PRODUCTO
-- --------------------

CREATE TABLE PRODUCTO (
  productoID integer PRIMARY KEY NOT NULL,
  precio float CHECK (precio > 0),
  stock integer,
  ventas integer,
  peliculaID integer NOT NULL,
  descripcion char(30)
);

ALTER TABLE PRODUCTO OWNER TO alumnodb;

CREATE SEQUENCE PRODUCTO_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE PRODUCTO_SEQ OWNER TO alumnodb;

ALTER SEQUENCE PRODUCTO_SEQ OWNED BY PRODUCTO.productoID;

-- --------------------
-- RELACION PRODUCTO - PELICULA
-- --------------------

CREATE TABLE PRODUCTO_PELICULA (
  productoID integer,
  peliculaID integer
);

ALTER TABLE PRODUCTO_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PEDIDO
-- --------------------

CREATE TABLE PEDIDO (
  pedidoID integer PRIMARY KEY NOT NULL,
  fecha date,
  total float CHECK (total > 0),
  estado char(15),
  clienteID integer NOT NULL
);

ALTER TABLE PEDIDO OWNER TO alumnodb;

CREATE SEQUENCE PEDIDO_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE PEDIDO_SEQ OWNER TO alumnodb;

ALTER SEQUENCE PEDIDO_SEQ OWNED BY PEDIDO.pedidoID;

-- --------------------
-- RELACION PEDIDO - PRODUCTO
-- --------------------

CREATE TABLE PEDIDO_PRODUCTO (
  pedidoID integer,
  productoID integer,
  precio float CHECK (precio > 0),
  cantidad integer
);

ALTER TABLE PEDIDO_PRODUCTO OWNER TO alumnodb;

-- --------------------
--  TABLA CLIENTE
-- --------------------

CREATE TABLE CLIENTE (
  clienteID integer PRIMARY KEY NOT NULL,
  username char(70),
  password char(70),
  nombre char(70),
  mail char(150),
  tarjeta char(16),
  cvc char(3),
  saldo float CHECK (saldo > 0)
);

ALTER TABLE CLIENTE OWNER TO alumnodb;

CREATE SEQUENCE CLIENTE_SEQ
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE CLIENTE_SEQ OWNER TO alumnodb;

ALTER SEQUENCE CLIENTE_SEQ OWNED BY CLIENTE.clienteID;

-- --------------------
-- POBLAMOS LA BASE DE DATOS
-- --------------------

INSERT INTO ACTOR (actorID, nombre)
SELECT actorid, actorname
FROM public.imdb_actors;

INSERT INTO ACTOR_PELICULA(actorID, peliculaID, personaje)
SELECT actorid, movieid, "character"
FROM public.imdb_actormovies;

INSERT INTO DIRECTOR (directorID, nombre)
SELECT directorid, directorname
FROM public.imdb_directors;

INSERT INTO DIRECTOR_PELICULA (directorID, peliculaID)
SELECT directorid, movieid
FROM public.imdb_directormovies;

INSERT INTO PELICULA (peliculaID, titulo, anno, puntuacion, sinopsis)
SELECT movieid, movietitle, year, 5,
  'Debajo un botón, ton, ton
  que encontró Martín, tin, tin
  había un ratón, ton, ton,
  ¡ay! que chiquitín, tin, tin.
  ¡Ay! que chiquitín, tin, tin,
  era aquel ratón, ton, ton,
  que encontró Martín, tin, tin,
  debajo un botón, ton, ton.'
FROM public.imdb_movies;

INSERT INTO GENERO_PELICULA (peliculaID, genero)
SELECT movieid, genre
FROM public.imdb_moviegenres;

INSERT INTO IDIOMA_PELICULA (peliculaID, idioma)
SELECT movieid, language
FROM public.imdb_movielanguages;

INSERT INTO PAIS_PELICULA (peliculaID, pais)
SELECT movieid, country
FROM public.imdb_moviecountries;

INSERT INTO PRODUCTO (productoID, precio, peliculaID, descripcion, stock, ventas)
SELECT public.products.prod_id, price, movieid, description, stock, sales
FROM public.products JOIN public.inventory
ON public.products.prod_id = public.inventory.prod_id;

-- INSERT INTO PRODUCTO (stock, ventas)
-- SELECT stock, sales
-- FROM public.inventory
-- WHERE prod_id = productoID;

INSERT INTO PEDIDO_PRODUCTO (pedidoID, productoID, precio, cantidad)
SELECT orderid, prod_id, price, quantity
FROM public.orderdetail;

INSERT INTO PEDIDO (pedidoID, fecha, total, estado, clienteID)
SELECT orderid, orderdate, totalamount, status, customerid
FROM public.orders;

INSERT INTO CLIENTE
SELECT customerid, username, password, firstname, email, creditcard, 000, 200
FROM public.customers;
