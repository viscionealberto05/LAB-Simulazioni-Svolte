#Query per i nodi

SELECT *
FROM circuits

SELECT
    rc.year,
    r.driverId,
    r.position
FROM races rc, results r
WHERE rc.raceId = r.raceId
  AND rc.circuitId = %s
  AND rc.year BETWEEN %s AND %s
ORDER BY rc.year, r.position

#Query per gli archi

WITH (SELECT
    rc.circuitId,
    COUNT(r.driverId) AS piloti_arrivati
FROM races rc, results r
WHERE rc.raceId = r.raceId
  AND rc.year BETWEEN %s AND %s
  AND r.position IS NOT NULL
GROUP BY rc.circuitId) as circuiti_piloti


SELECT
    c1.circuitId AS circuito1,
    c2.circuitId AS circuito2,
    c1.piloti_arrivati + c2.piloti_arrivati AS peso
FROM circuiti_piloti c1, circuiti_piloti c2
WHERE c1.circuitId < c2.circuitId