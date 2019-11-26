CREATE OR REPLACE FUNCTION getTopVentas(anno text)
RETURNS TABLE(
	year text,
	movieid integer,
	movietitle character varying(500),
	sales integer) AS $topVentas$ BEGIN
RETURN QUERY(
	-- Tomamos la primera película que aparezca en caso de que para un mismo año
	-- haya más de una película con el mismo número de ventas
	SELECT *
		FROM (
			SELECT mov.year, (array_agg(mov.movieid ORDER BY inventory.sales)) [1] as movieid, (array_agg(mov.movietitle ORDER BY inventory.sales)) [1] as movietitle, MAX(inventory.sales) as sales
			FROM (imdb_movies mov JOIN products ON mov.movieid = products.movieid)
			JOIN inventory ON products.prod_id = inventory.prod_id
			GROUP BY mov.year) AS T1
		WHERE T1.year >= $1
);
END;
$topVentas$ language plpgsql;
