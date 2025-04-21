import pymysql
from flask import json
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)


def insert_data_to_db(json_data, db_config):
    connection = pymysql.connect(**db_config)
    print(json.dumps(json_data, indent=4))    
    try:
        with connection.cursor() as cursor:
            # Insert into the main table (assuming it's named `ofertas`)
            oferta_num = json_data['ofertaNum']
            datainit=json_data['DataPublicacao']
            data_inicio = datainit.split('T')[0]
            dataend = json_data['DataConclusao']
            data_fim = dataend.split('T')[0]
            
           
            for candidato in json_data['candidatosAdimitidosExcluidos']:
                candidato_nome = candidato['candidatoNome']
                candidato_nif = candidato['candidatoNIF']
                local_prova_nome = candidato['localProvaNome']
                candidato_email = candidato['candidatoEmail']
                candidato_telemovel = candidato['candidatoTelemovel']
                candidato_admitido = str(candidato.get('WasAdmitido')).lower()
                deficiencia = str(candidato.get('hasDeficiencia')).lower()  # Convert to string and lowercase
                if deficiencia == 'true':
                    candidato_deficiencia = 'sim'
                else:
                    candidato_deficiencia = 'não'
                    
                
                candidato_query = """
                    INSERT INTO admitidos_excluidos (candidato_nome,candidato_nif,local_prova_nome,candidato_email,candidato_telemovel,candidato_admitido,deficiencia,oferta_num)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(candidato_query, (candidato_nome,candidato_nif,local_prova_nome,candidato_email,candidato_telemovel,candidato_admitido,candidato_deficiencia,oferta_num))
                
                
        
        # Commit the transaction
        connection.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()


