import pymysql
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)

def get_user_info(bolsa_id, user_ids,oferta_num):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Create placeholders for the list of user_ids
        placeholders = ', '.join(['%s'] * len(user_ids))
        
        # Query to fetch user information where the user is linked to the correct bolsa_id
        query = f"""
        SELECT DISTINCT 
            u.id AS candidato_id, 
            u.nome, 
            u.avaliacao_curricular, 
            u.prova_de_conhecimentos, 
            u.nota_final, 
            c.tipo AS tipo_contrato, 
            u.estado
        FROM users u
        JOIN userbolsas ub ON u.id = ub.user_id
        LEFT JOIN contrato c ON ub.contrato_id = c.id
        WHERE u.id IN ({placeholders}) 
        AND ub.Bolsa_id = %s  
        AND u.oferta_num = %s
        ORDER BY u.nota_final DESC
        """
        # Add bolsa_id as the last parameter in the query execution
        cursor.execute(query, user_ids + [bolsa_id,oferta_num])
        results = cursor.fetchall()

        # Return results as a list of dictionaries, including tipo_contrato
        return [{
            "id": row[0], 
            "nome": row[1], 
            "avaliacao_curricular": row[2], 
            "prova_de_conhecimentos": row[3], 
            "nota_final": row[4],
            "tipo_contrato": row[5],  # Include tipo_contrato
            "estado": row[6]
        } for row in results]

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        cursor.close()
        connection.close()
        
def user_infos(user_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        query = """
        SELECT u.id AS candidato_id, u.nome, u.contacto, u.deficiencia, 
               u.avaliacao_curricular, u.prova_de_conhecimentos, u.nota_final, 
               u.estado, u.observacoes, u.distribuicao, u.NIF, u.local_prova, u.oferta_num, u.email,
               d.file_name, d.upload_date
        FROM users u
        LEFT JOIN documents d ON u.id = d.user_id
        WHERE u.id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        if not result:
            return {}  # Return empty dictionary if no user is found

        # Extract user information from the first row
        user_info = {
            "id": result[0][0],
            "nome": result[0][1],
            "contacto": result[0][2],
            "deficiencia": result[0][3],
            "avaliacao_curricular": result[0][4],
            "prova_de_conhecimentos": result[0][5],
            "nota_final": result[0][6],
            "estado": result[0][7],
            "observacoes": result[0][8],
            "distribuicao": result[0][9],
            "NIF": result[0][10],
            "local_prova": result[0][11],
            "oferta_num": result[0][12],
            "email": result[0][13],
            "documentos": []  # Initialize empty list for documents
        }

        # Append documents if they exist
        for row in result:
            file_name = row[14]
            upload_date = row[15]
            if file_name and upload_date:  # Check if both values are present
                user_info["documentos"].append({
                    "file_name": file_name,
                    "upload_date": upload_date
                })

        return user_info

    except Exception as e:
        print(f"Error: {e}")
        return {}

    finally:
        cursor.close()
        connection.close()


def get_colocados_by_user_id(user_id):
    connection = connect_to_database()  # Ensure this function is defined elsewhere
    cursor = connection.cursor()

    query = """
    SELECT 
        c.id, 
        c.user_id, 
        b.nome AS bolsa_nome, 
        c.escola_nome, 
        co.tipo AS tipo_contrato, 
        c.escola_priority_id, 
        c.placement_date,
        c.estado,
        c.alterado_por 
    FROM colocados AS c
    LEFT JOIN Bolsa AS b ON c.bolsa_id = b.id
    LEFT JOIN contrato AS co ON c.contrato_id = co.id
    WHERE c.user_id = %s
    ORDER BY c.placement_date DESC
    """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    colocados_list = [
        {
            "id": row[0],
            "user_id": row[1],
            "bolsa_nome": row[2],
            "escola_nome": row[3],
            "tipo_contrato": row[4],
            "escola_priority_id": row[5],
            "placement_date": row[6],
            "estado": row[7],  # Add estado to the result dictionary
            "alterado_por": row[8]
        }
        for row in results
    ]

    cursor.close()
    connection.close()

    return colocados_list
        
def get_colocados(curr_oferta):
    connection = connect_to_database()  # Ensure this function is defined elsewhere
    cursor = connection.cursor()

    query = """
    SELECT 
        c.id, 
        c.user_id, 
        b.nome AS bolsa_nome, 
        c.escola_nome, 
        co.tipo AS tipo_contrato, 
        c.escola_priority_id, 
        c.placement_date,
        c.estado  
    FROM colocados AS c
    LEFT JOIN Bolsa AS b ON c.bolsa_id = b.id
    LEFT JOIN contrato AS co ON c.contrato_id = co.id
    WHERE c.oferta_num = %s
    ORDER BY c.placement_date DESC
    """
    cursor.execute(query,(curr_oferta))
    results = cursor.fetchall()

    colocados_list = [
        {
            "id": row[0],
            "user_id": row[1],
            "bolsa_nome": row[2],
            "escola_nome": row[3],
            "tipo_contrato": row[4],
            "escola_priority_id": row[5],
            "placement_date": row[6],
            "estado": row[7],  # Add estado to the result dictionary
        }
        for row in results
    ]

    cursor.close()
    connection.close()

    return colocados_list        

def count_users_by_bolsa(bolsa_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    SELECT COUNT(*) FROM listas WHERE bolsa_id = %s
    """
    cursor.execute(query, (bolsa_id,))
    total = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return total

def update_additional_info(user_id, additional_info):
    
    connection = connect_to_database()
    cursor = connection.cursor()
    
    query = """
        UPDATE users
        SET observacoes = %s
        WHERE id = %s
    """
    cursor.execute(query, (additional_info, user_id))
    connection.commit()
    cursor.close()
    connection.close()

def get_escola_info(escola_nome):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        query = """
            SELECT * FROM escola WHERE nome = %s
        """
        cursor.execute(query, (escola_nome,))
        escola_info = cursor.fetchone()  # Fetch the first matching record

        if escola_info:
            columns = [col[0] for col in cursor.description]  # Get column names
            escola_info_dict = dict(zip(columns, escola_info))
            return escola_info_dict

        return None  # If no result is found, return None
    except Exception as e:
        print(f"Error retrieving escola info: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
    
    
