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

def select_ofertas_lista():
    connection = connect_to_database()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT DISTINCT oferta_num FROM users
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
        

def get_admins():
    connection = connect_to_database()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to return dictionaries
    try:
        query = """
        SELECT id, username, email, updated_at FROM Admin
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Return the list of admin details directly
        return results
    except pymysql.MySQLError as e:
        print(f"Error while executing query: {e}")
        return []  # Return an empty list if an error occurs
    finally:
        cursor.close()
        connection.close()
        
def add_admins(username,password,email):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        query= """
        INSERT INTO Admin(username,password,email) VALUES(%s,%s,%s)
        """
        cursor.execute(query(username,password,email))
        
    except pymysql.MySQLError as e :
        return []
    finally:
        cursor.close()
        connection.close()