#Query per i nodi

SELECT p.id, p.name
FROM player p, actions a, matches m
WHERE a.player_id = p.id and m.matchId = a.matchId
GROUP BY p.id, p.name
HAVING (SUM(a.goals) / COUNT(DISTINCT a.matchId)) >= %s


#Query per gli archi

SELECT p1.id, p2.id, SUM(a1.TimePlayed) as t1, SUM(a2.TimePlayed) as T2
FROM player p1, player p2, actions a1, actions a2
WHERE a1.player_id = p1.id and a2.player_id = p2.id
    and a1.matchId = a2.matchId and p1.id < p2.id
    and a1.teamId != a2.teamId
    and a1.starts = 1 and a2.starts = 1
GROUP BY p1.id, p2.id