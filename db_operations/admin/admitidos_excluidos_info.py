import pymysql
from flask import json
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)


def insert_data_to_db(json_data, db_config):
    try:
        connection = pymysql.connect(**db_config)
        print(json.dumps(json_data, indent=4))    
        try:
            with connection.cursor() as cursor:
                # Extract main offer data
                bolsa_ilha_data = json_data.get("API_Expose_BolsaIlha_AE", {})
                oferta_num = bolsa_ilha_data.get('ofertaNum')
                data_publicacao = bolsa_ilha_data.get('DataPublicacao', '').split('T')[0]
                data_conclusao = bolsa_ilha_data.get('DataConclusao', '').split('T')[0]

                # Ensure candidates exist in the data
                candidatos = bolsa_ilha_data.get('CandidatosAdimitidosExcluidos', [])
                if not candidatos:
                    print("No candidates found in the provided data.")
                    return
                
                for candidato in candidatos:
                    # Extract candidate data with fallback values
                    candidato_nome = candidato.get('candidatoNome', '')
                    candidato_nif = candidato.get('candidatoNIF', '')
                    local_prova_nome = candidato.get('localProvaNome', '')
                    candidato_email = candidato.get('candidatoEmail', '')
                    candidato_telemovel = candidato.get('candidatoTelemovel', '')
                    candidato_admitido = str(candidato.get('WasAdmitido', False))
                    has_deficiencia = str(candidato.get('hasDeficiencia', False)).lower()
                    
                    # Convert deficiencia to "sim" or "não"
                    deficiencia_status = "sim" if has_deficiencia == "true" else "não"

                    # SQL query to insert data
                    candidato_query = """
                        INSERT INTO admitidos_excluidos (
                            candidato_nome, candidato_nif, local_prova_nome, 
                            candidato_email, candidato_telemovel, candidato_admitido, 
                            deficiencia, oferta_num
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    # Execute the query
                    cursor.execute(candidato_query, (
                        candidato_nome, candidato_nif, local_prova_nome, 
                        candidato_email, candidato_telemovel, candidato_admitido, 
                        deficiencia_status, oferta_num
                    ))
                
                # Commit the transaction
                connection.commit()
                print("Data inserted successfully.")

        except Exception as e:
            print(f"Error while inserting data: {e}")
            connection.rollback()
        
        finally:
            connection.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")


