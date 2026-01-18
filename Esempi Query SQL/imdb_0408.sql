#Query per i nodi

SELECT a.id
FROM actors a, roles r, movies_genres g
WHERE r.actor_id = a.id and r.movie_id = g.movie_id and g.genre = %s

#Query per gli archi

SELECT r1.actor_id, r2.actor_id, COUNT(DISTINCT(r1.movie_id)) as weight
FROM roles r1, roles r2, movies_genres g
WHERE r1.movie_id = r2.movie_id and
    r1.movie_id = g.movie_id and
    r1.actor_id < r2.actor_id and
    g.genre = %s
GROUP BY r1.actor_id, r2.actor_id