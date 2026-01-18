from database.DB_connect import DBConnect
from model.stato import Stato
class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(YEAR(s_datetime)) as year
                    FROM sighting
                    WHERE YEAR(s_datetime) >= 1910 and YEAR(s_datetime) <= 2014"""

        cursor.execute(query)

        for row in cursor:
            result.append(int(row["year"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(shape)
                    FROM sighting
                    WHERE shape != '' """

        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_stati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM state"""

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges(year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query1 = """ SELECT LEAST(n.state1, n.state2) as st1, GREATEST(n.state1, n.state2) as st2, COUNT(*) as weight
                    FROM neighbor n, sighting s
                    WHERE (n.state1 = s.state OR n.state2 = s.state) AND
                        YEAR(s.s_datetime) = %s AND
                        s.shape = %s
                    GROUP BY st1, st2"""

        query = """ SELECT LEAST(n.state1, n.state2) AS st1,
                           GREATEST(n.state1, n.state2) AS st2, 
                           (COUNT(*)/2) as weight
                    FROM sighting s , neighbor n 
                    WHERE year(s.s_datetime) = %s
                          AND s.shape = %s
                          AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY st1 , st2 """

        cursor.execute(query, [year, shape],)

        for row in cursor:
            result.append([row["st1"], row["st2"], row["weight"]])

        cursor.close()
        conn.close()
        return result
