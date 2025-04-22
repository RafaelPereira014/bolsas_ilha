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

        # Extract only the `oferta_num` values as a list
        ofertas = [row['oferta_num'] for row in results]
        return ofertas  # Return a list of oferta_num values
    except pymysql.MySQLError as e:
        print(f"Error while executing query: {e}")
        return []  # Return an empty list if an error occurs
    finally:
        cursor.close()
        connection.close()
        