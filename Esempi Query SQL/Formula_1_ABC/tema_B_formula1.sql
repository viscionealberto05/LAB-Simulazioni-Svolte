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


WITH circuiti_pilotind as (SELECT rc.circuitId, COUNT(DISTINCT(r.driverId)) as piloti_non_doppiati
FROM races rc, results r
WHERE rc.raceId = r.raceId and
    r.time is NOT NULL and
    rc.year BETWEEN %s and %s
GROUP by rc.circuitId)

SELECT cp1.circuitId, cp2.circuitId, (cp1.piloti_non_doppiati + cp2.piloti_non_doppiati) as w
FROM circuiti_pilotind cp1, circuiti_pilotind cp2
WHERE cp1.circuitId < cp2.circuitId
GROUP BY cp1.circuitId, cp2.circuitId

