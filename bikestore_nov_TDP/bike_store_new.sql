#query archi

SELECT o1.id, o2.id, ((SUM(oi1.quantity) + SUM(oi2.quantity)) / DATEDIFF(o1.order_date, o2.order_date)) as w
FROM order o1, order o2, order_items oi1, order_items oi2
WHERE o1.store_id = o2.store_id
    and o1.store_id = %s
    and DATEDIFF(o1.order_date, o2.orderdate) <= %s
    and o1.order_date < o2.order_date
    and oi1.order_id = o1.id 
    and oi2.order_id = o2.id 
GROUP BY o1.id, o2.id

oppure, più logico ma che richiede maggior lavoro nell elaborazione dati:

SELECT 
    o1.id AS id1, 
    o2.id AS id2,
    SUM(oi1.quantity) AS q1, 
    SUM(oi2.quantity) AS q2, 
    DATEDIFF(o2.order_date, o1.order_date) AS diff_data
FROM `order` o1, `order` o2, order_items oi1, order_items oi2
WHERE o1.store_id = o2.store_id
    AND o1.store_id = %s
    AND o1.id != o2.id
    AND ABS(DATEDIFF(o2.order_date, o1.order_date)) <= %s
    AND oi1.order_id = o1.id
    AND oi2.order_id = o2.id
GROUP BY o1.id, o2.id;


if diff_data > 0:
    source = o1
    target = o2
else:
    source = o2
    target = o1
