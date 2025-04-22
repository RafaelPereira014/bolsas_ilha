import csv
import pymysql
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)


def select_ofertas():
    connection = connect_to_database()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT DISTINCT oferta_num FROM admitidos_excluidos
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results  # Return the results for further use
    except pymysql.MySQLError as e:
        print(f"Error while executing query: {e}")
    finally:
        cursor.close()
        connection.close()
        