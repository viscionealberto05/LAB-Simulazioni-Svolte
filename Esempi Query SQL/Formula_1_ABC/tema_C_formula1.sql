#Query per i nodi

SELECT *
FROM constructors

SELECT r.constructorId, rc.year, r.driverId, r.position
FROM results r, races rc
WHERE rc.year BETWEEN %s and %s and
    r.raceId = rc.raceId

#Query per gli archi

WITH costruttore_peso AS (
    SELECT
        r.constructorId,
        COUNT(*) AS w
    FROM results r, races rc
    WHERE r.raceId = rc.raceId
      AND rc.year BETWEEN %s AND %s
      AND r.position IS NOT NULL
    GROUP BY r.constructorId
)


SELECT
    cp1.constructorId AS team1,
    cp2.constructorId AS team2,
    cp1.w + cp2.w AS peso
FROM costruttore_peso cp1, costruttore_peso cp2
WHERE cp1.constructorId < cp2.constructorId




"""SELECT cp1.constructorId, cp2.constructorId, (cp1.w + cp2.w) as w
FROM results r1, results r2, races rc, costruttore_peso cp1, costruttore_peso cp2
WHERE rc.raceId = r1.raceId and rc.raceId = r2.raceId and
    rc.year BETWEEN %s and %s and
    cp1.constructorId = r1.constructorId and
    cp2.constructorId = r2.constructorId and
    cp1.constructorId < cp2.constructorId


WITH costruttore_peso as(
    SELECT r.constructorId, COUNT(*) as w
    FROM results r, races rc
    WHERE r.raceId = rc.raceId and
        rc.year BETWEEN %s and %s and
        r.position is not NULL
    GROUP BY constructorId
)"""