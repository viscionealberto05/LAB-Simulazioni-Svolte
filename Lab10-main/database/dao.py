from database.DB_connect import DBConnect
from model.tratta import Tratta
from model.hub import Hub

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
    def get_hub():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * \
                    FROM hub """

        cursor.execute(query)

        for row in cursor:
            result.append(Hub(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_tratta():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id_hub_origine as id_hub_1, id_hub_destinazione as id_hub_2, sum(valore_merce) as somma_tratta, count(*) as n_spedizioni
                    FROM spedizione
                    GROUP BY id_hub_origine, id_hub_destinazione
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(**row))

        cursor.close()
        conn.close()
        return result
