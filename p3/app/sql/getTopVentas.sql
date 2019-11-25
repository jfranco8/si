CREATE OR REPLACE FUNCTION getTopVentas(year text)
RETURNS TABLE(
	anno text,
	titulo character varying(500),
	ventas integer) AS $topVentas$ BEGIN
RETURN QUERY(
	-- Tomamos la primera película que aparezca en caso de que para un mismo año
	-- haya más de una película con el mismo número de ventas
	SELECT T1.year, (array_agg(T1.movietitle ORDER BY T1.sales)) [1], MAX(T1.sales)
	FROM ((imdb_movies JOIN products ON imdb_movies.movieid = products.movieid)
		JOIN inventory ON products.prod_id = inventory.prod_id) AS T1
	WHERE T1.year >= $1
	GROUP BY T1.year
);
END;
$topVentas$ language plpgsql;
