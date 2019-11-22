
----------------------------
----- BORRAMOS LA DB ANTERIOR
----------------------------

DROP TABLE
  public.country,
  public.genres;

----------------------------
----- CLAVES EXTRANJERAS
----------------------------

ALTER TABLE public.imdb_actormovies
ADD FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);

ALTER TABLE public.imdb_actormovies
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

ALTER TABLE public.imdb_directormovies
ADD FOREIGN KEY (directorid) REFERENCES imdb_directors(directorid);

ALTER TABLE public.imdb_actormovies
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

ALTER TABLE public.products
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE public.orderdetail
ADD FOREIGN KEY (orderid) REFERENCES orders(orderid);

ALTER TABLE public.orderdetail
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE public.inventory
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);

ALTER TABLE public.orders
ADD FOREIGN KEY (customerid) REFERENCES customers(customerid);

ALTER TABLE public.products
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);


----------------------------
----- MOVIE COUNTRIES
----------------------------

CREATE TABLE public.country (
  countryid integer NOT NULL PRIMARY KEY,
  country char(40) NOT NULL
);

ALTER TABLE public.country OWNER TO alumnodb;

CREATE SEQUENCE COUNTRY_NEW_SEQ
    START 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

ALTER TABLE COUNTRY_NEW_SEQ OWNER TO alumnodb;

ALTER SEQUENCE COUNTRY_NEW_SEQ OWNED BY public.country.countryid;

ALTER TABLE public.country ALTER COLUMN countryid SET DEFAULT nextval('COUNTRY_NEW_SEQ'::regclass);

CREATE TABLE public.movie_country (
  countryid integer,
  movieid integer
);

INSERT INTO public.country (country)
SELECT DISTINCT country
FROM public.imdb_moviecountries;

INSERT INTO public.movie_country
SELECT countryid, movieid
FROM public.country, public.imdb_moviecountries
WHERE public.country.country = public.imdb_moviecountries.country;

ALTER TABLE public.movie_country
ADD FOREIGN KEY (countryid) REFERENCES country(countryid);

ALTER TABLE public.movie_country
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

----------------------------
----- MOVIE genres
----------------------------

CREATE TABLE public.genres (
  genreid integer NOT NULL PRIMARY KEY,
  genre char(40) NOT NULL
);

ALTER TABLE public.genres OWNER TO alumnodb;

CREATE SEQUENCE GENRE_NEW_SEQ
    START 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

ALTER TABLE GENRE_NEW_SEQ OWNER TO alumnodb;

ALTER SEQUENCE GENRE_NEW_SEQ OWNED BY public.genres.genreid;

ALTER TABLE public.genres ALTER COLUMN genreid SET DEFAULT nextval('GENRE_NEW_SEQ'::regclass);

CREATE TABLE public.movie_genre (
  genreid integer,
  movieid integer
);

INSERT INTO public.genres (genre)
SELECT DISTINCT genre
FROM public.imdb_moviegenres;

INSERT INTO public.movie_genre
SELECT genreid, movieid
FROM public.genres, public.imdb_moviegenres
WHERE public.genres.genre = public.imdb_moviegenres.genre;

ALTER TABLE public.movie_genre
ADD FOREIGN KEY (genreid) REFERENCES genres(genreid);

ALTER TABLE public.movie_genre
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);
