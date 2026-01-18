#Query per i nodi

SELECT *
FROM go_products
WHERE Product_brand = %

#Query per gli archi

SELECT s1.Product_number, s2.Product_number, count(DISTINCT(r.Retailer_code)) as weight
FROM go_daily_sales s1, go_daily_sales s2
WHERE YEAR(s1.date) = %s and YEAR(s2.date) = %s and
    s1.date = s2.date and
    s1.Product_number < s2.Product_number and
    s1.Retailer_code = s2.Retailer_code and
GROUP BY s1.Product_number, s2.Product_number