
----------------------------
----- BORRAMOS LA DB ANTERIOR
----------------------------

DROP TABLE
  public.country,
  public.genres,
  public.languages;

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

CREATE TABLE IF NOT EXISTS public.country (
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

CREATE TABLE IF NOT EXISTS public.movie_country (
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
----- MOVIE GENRES
----------------------------

CREATE TABLE IF NOT EXISTS public.genres (
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

CREATE TABLE IF NOT EXISTS public.movie_genre (
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

----------------------------
----- MOVIE LANGUAGES
----------------------------

CREATE TABLE IF NOT EXISTS public.languages (
  languageid integer NOT NULL PRIMARY KEY,
  language char(40) NOT NULL
);

ALTER TABLE public.languages OWNER TO alumnodb;

CREATE SEQUENCE LANGUAGE_NEW_SEQ
    START 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

ALTER TABLE LANGUAGE_NEW_SEQ OWNER TO alumnodb;

ALTER SEQUENCE LANGUAGE_NEW_SEQ OWNED BY public.languages.languageid;

ALTER TABLE public.languages ALTER COLUMN languageid SET DEFAULT nextval('LANGUAGE_NEW_SEQ'::regclass);

CREATE TABLE IF NOT EXISTS public.movie_language (
  languageid integer,
  movieid integer
);

INSERT INTO public.languages (language)
SELECT DISTINCT language
FROM public.imdb_movielanguages;

INSERT INTO public.movie_language
SELECT languageid, movieid
FROM public.languages, public.imdb_movielanguages
WHERE public.languages.language = public.imdb_movielanguages.language;

ALTER TABLE public.movie_language
ADD FOREIGN KEY (languageid) REFERENCES languages(languageid);

ALTER TABLE public.movie_language
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

----------------------------
----- TABLE CUSTOMER
----------------------------

ALTER TABLE public.customers
ADD IF NOT EXISTS cvc character varying(3);

UPDATE public.customers
SET cvc = '000';
