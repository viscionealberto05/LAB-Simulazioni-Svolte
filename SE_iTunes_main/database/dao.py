from database.DB_connect import DBConnect
from model.album import Album
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
    def get_album(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id, a.title, a.artist_id
                    FROM album a, track t
                    WHERE a.id = t.album_id
                    GROUP BY a.id, a.title, a.artist_id
                    HAVING SUM(t.milliseconds) > %s"""

        cursor.execute(query, [durata*60*1000],)

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_durate(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id, SUM(t.milliseconds) as durata
                    FROM album a, track t
                    WHERE a.id = t.album_id
                    GROUP BY a.id
                    HAVING SUM(t.milliseconds) > %s"""

        cursor.execute(query, [durata * 60 * 1000], )

        for row in cursor:
            result.append((row["id"], float(row["durata"])/(1000*60)))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t1.album_id as a1, t2.album_id as a2
                    FROM track t1, track t2, playlist_track pt1, playlist_track pt2
                    WHERE t1.album_id != t2.album_id and t1.id = pt1.track_id and t2.id = pt2.track_id and pt1.playlist_id = pt2.playlist_id
                    GROUP BY t1.album_id, t2.album_id
                    HAVING count(*) >0
         """

        cursor.execute(query)

        for row in cursor:
            result.append((int(row['a1']),int(row['a2'])))

        cursor.close()
        conn.close()
        return result
