#Query per ottenere i nodi

#Considero i risultati raggruppati per costruttore, per pilota, con la data corretta
#e che siano coerenti con l aver tagliato il traguardo. Group by equivale al distinct

SELECT r.constructorId
FROM results r, races rc
WHERE r.position is NOT NULL and rc.raceId = r.raceId and rc.year <= %s and rc.year >= %s
GROUP BY r.constructorId

#Successivamente da una mappa dei costruttori associare l oggetto costruttore e ottenere il nodo

#Query per ottenere gli archi, a partire dalle coppie di gare in cui il costruttore e la gara erano diversi, ma il driver lo stesso,
#che ha finito la gara, e nell anno richiesto

SELECT res1.constructorId, res2.constructorId,  COUNT(DISTINCT res1.driverId) AS weight
FROM results res1, results res2, races rc1, races rc2
WHERE rc1.year <= %s and rc1.year >= %s 
        and rc2.year <= %s and rc2.year >= %s 
        and res1.driverId = res2.driverId 
        and res1.constructorId < res2.constructorId 
        and res1.raceId = rc1.raceId 
        and res2.raceId = rc2.raceId 
        and res1.raceId != res2.raceId 
        and res1.position is NOT NULL 
        and res2.position is NOT NULL
GROUP BY res1.constructorId, res2.constructorId
