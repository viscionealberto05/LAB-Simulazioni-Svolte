from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categories():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM category"""

        cursor.execute(query)

        for row in cursor:
            result.append(Category(**row))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_products(id_categoria):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM product
                    WHERE category_id = %s """

        cursor.execute(query, [id_categoria],)

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_prodotti_venduti(id_categoria,data_inizio, data_fine):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.id as id_prodotto, COUNT(*) as vendite
                    FROM product p, order_item oi, `order` o
                    WHERE p.id = oi.product_id AND oi.order_id = o.id AND p.category_id = %s AND o.order_date >= %s AND o.order_date <= %s
                    GROUP BY p.id
                    HAVING COUNT(*) > 0 """

        cursor.execute(query, [id_categoria, data_inizio, data_fine])

        for row in cursor:
            result.append((row["id_prodotto"], row["vendite"])) #lista di tuple

        cursor.close()
        conn.close()
        return result


