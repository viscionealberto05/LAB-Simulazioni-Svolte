#Query per i nodi

SELECT *
FROM portions
WHERE calories < %s

#Query per gli archi

SELECT p1.portion_id, p2.portion_id, COUNT(DISTINCT(f.food_code)) as weight
FROM portion p1, portion p2, food f
WHERE f.food_code = p1.food_code and f.food_code = p2.food_code
      and p1.portion_id < p2.portion_id and p1.calories < %s and p2.calories < %s
GROUP BY p1.portion_id, p2.portion_id