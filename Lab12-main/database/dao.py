from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione
class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * \
                    FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_rifugi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM rifugio """

        cursor.execute(query)

        for row in cursor:
            result.append(Rifugio(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM connessione
                    WHERE anno <= %s"""

        cursor.execute(query, [int(anno)],)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result