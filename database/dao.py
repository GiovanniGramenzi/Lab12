from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio
class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def get_rifugi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = 'SELECT * FROM rifugio'
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(
                Rifugio(row['id'], row['nome'], row['localita'], row['altitudine'], row['capienza'], row['aperto']))
        cursor.close()
        cnx.close()
        return result
    @staticmethod
    def get_connessioni(anno_max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = '''SELECT id_rifugio1,id_rifugio2,distanza,difficolta
        FROM connessione
        WHERE anno<%s'''
        cursor.execute(query, (anno_max,))
        result = []
        for row in cursor:
            result.append(Connessione(row['id_rifugio1'], row['id_rifugio2'],row['distanza'],row['difficolta']))
        cursor.close()
        cnx.close()
        return result
