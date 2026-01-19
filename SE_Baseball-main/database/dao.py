from database.DB_connect import DBConnect
from model.team import Team

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
        query = """ SELECT DISTINCT year 
                    FROM team
                    WHERE year >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_squadre(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM team
                    WHERE year = %s"""

        cursor.execute(query, [year],)

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_salari(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s.team_id as team_id, sum(s.salary) as salary
                    FROM salary s
                    WHERE s.year = %s
                    GROUP BY s.team_id"""

        cursor.execute(query, [year],)

        for row in cursor:
            result.append([row["team_id"], row["salary"]])

        cursor.close()
        conn.close()
        return result

