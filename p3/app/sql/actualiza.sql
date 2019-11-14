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
  actor integer FOREIGN KEY NOT NULL REFERENCES ACTOR.actorID,
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID,
  personaje char(70)
);

ALTER TABLE ACTOR_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PELICULA
-- --------------------

CREATE TABLE PELICULA (
  peliculaID integer PRIMARY KEY NOT NULL,
  titulo char(100),
  trailer char(100),
  sinopsis char(10000),
  puntuacion integer,
  anno integer,
  is_mas_vistas boolean,
  is_novedades boolean
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
  nombre char(70)
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
  director integer FOREIGN KEY NOT NULL REFERENCES DIRECTOR.directorID,
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID
);

ALTER TABLE DIRECTOR_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION GENERO - PELICULA
-- --------------------

CREATE TABLE GENERO_PELICULA (
  genero char(70),
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID
);

ALTER TABLE GENERO_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION IDIOMA - PELICULA
-- --------------------

CREATE TABLE IDIOMA_PELICULA (
  idioma char(70),
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID
);

ALTER TABLE IDIOMA_PELICULA OWNER TO alumnodb;

-- --------------------
-- RELACION PAIS - PELICULA
-- --------------------

CREATE TABLE PAIS_PELICULA (
  pais char(70),
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID
);

ALTER TABLE PAIS_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PRODUCTO
-- --------------------

CREATE TABLE PRODUCTO (
  productoID integer PRIMARY KEY NOT NULL,
  precio float,
  stock integer,
  ventas integer
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
  producto integer FOREIGN KEY NOT NULL REFERENCES PRODUCTO.productoID,
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID
);

ALTER TABLE PRODUCTO_PELICULA OWNER TO alumnodb;

-- --------------------
--  TABLA PEDIDO
-- --------------------

CREATE TABLE PEDIDO (
  pedidoID integer PRIMARY KEY NOT NULL,
  fecha date,
  total float,
  estado boolean
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
-- RELACION PEDIDO - PELICULA
-- --------------------

CREATE TABLE PEDIDO_PELICULA (
  pedido integer FOREIGN KEY NOT NULL REFERENCES PEDIDO.pedidoID,
  pelicula integer FOREIGN KEY NOT NULL REFERENCES PELICULA.peliculaID,
  precio float,
  cantidad integer
);

ALTER TABLE PEDIDO_PELICULA OWNER TO alumnodb;

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
  saldo float
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
-- RELACION CLIENTE - PEDIDO
-- --------------------

CREATE TABLE CLIENTE_PEDIDO (
  pedido integer FOREIGN KEY NOT NULL REFERENCES PEDIDO.pedidoID,
  cliente integer FOREIGN KEY NOT NULL REFERENCES CLIENTE.clienteID
);

ALTER TABLE CLIENTE_PEDIDO OWNER TO alumnodb;

-- FALTA POBLAR LA BASE DE DATOS
