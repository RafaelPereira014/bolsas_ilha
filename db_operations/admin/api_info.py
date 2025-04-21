import pymysql
from flask import json
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(**db_config)

def get_id_contrato(tipo_de_vinculo):
    contrato_mapping = {
        "CTFP por tempo Indeterminado - Bolsa de Ilha": 1,
        "CTFP a termo resolutivo - Bolsa de Ilha": 2,
        "CTFP ambos  - Bolsa de Ilha": 3
    }
    return contrato_mapping.get(tipo_de_vinculo, None)

def get_escola_id(codigo_de_escola):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT id FROM escola WHERE cod_est = %s"
            cursor.execute(query, (codigo_de_escola,))
            result = cursor.fetchone()  
            
            if result:
                return result[0]  
            else:
                return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        connection.close()

def insert_data_to_db(json_data, db_config):
    connection = pymysql.connect(**db_config)
    print(json.dumps(json_data, indent=4))    
    try:
        with connection.cursor() as cursor:
            # Insert into the main table (assuming it's named `ofertas`)
            oferta_num = json_data['ofertaNum']
            oferta_ano = 2025
            datainit=json_data['DataPublicacao']
            data_inicio = datainit.split('T')[0]
            dataend = json_data['DataConclusao']
            data_fim = dataend.split('T')[0]
            
            oferta_query = """
                INSERT INTO oferta (oferta_num, oferta_ano, data_inicio, data_fim)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(oferta_query, (oferta_num, oferta_ano, data_inicio, data_fim))
            for candidato in json_data['candidatos']:
                candidato_nome = candidato['candidatoNome']
                candidato_nif = candidato['candidatoNIF']
                local_prova_nome = candidato['localProvaNome']
                candidato_email = candidato['candidatoEmail']
                candidato_telemovel = candidato['candidatoTelemovel']
                candidato_aval_curricular = candidato['NotaAvCurricular']
                candidato_prova_conhecimentos = candidato['NotaProvaConhecimentos']
                if candidato['candidatoNotaFinal'] >= 9.5:
                    candidato_nota_final = candidato['candidatoNotaFinal']
                deficiencia = str(candidato.get('hasDeficiencia')).lower()  # Convert to string and lowercase
                if deficiencia == 'true':
                    candidato_deficiencia = 'sim'
                else:
                    candidato_deficiencia = 'não'
                    
                Estado = 'livre'
                
                candidato_query = """
                    INSERT INTO users (oferta_num, nome, nif, local_prova, deficiencia,contacto, avaliacao_curricular, prova_de_conhecimentos, nota_final,estado)
                    VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s,%s)
                """
                cursor.execute(candidato_query, (
                    oferta_num, candidato_nome, candidato_nif, local_prova_nome,
                    candidato_deficiencia,candidato_telemovel,
                    candidato_aval_curricular, candidato_prova_conhecimentos, candidato_nota_final,Estado
                ))
                candidato_id = cursor.lastrowid
                
                for preferencia in candidato['preferenciasPorCandidato']:
                    ilha_id = preferencia['ilhaId']
                    tipo_de_vinculo = preferencia['tipoDeVinculo']
                    id_vinculo = get_id_contrato(tipo_de_vinculo)
                    codigo_de_escola = preferencia['codigoDeEscola']
                    id_escola = get_escola_id(codigo_de_escola)
                    ordem_de_preferencia = preferencia['ordemDePreferencia']
                    
                    bolsa_query = """
                        INSERT INTO userbolsas (user_id, Bolsa_id, contrato_id)
                        VALUES (%s, %s, %s)
                    """
                    preferencia_query = """
                        INSERT INTO user_escola (user_id, escola_id, escola_priority_id)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(bolsa_query, (
                        candidato_id, ilha_id, id_vinculo
                    ))
                    cursor.execute(preferencia_query, (
                        candidato_id, id_escola, ordem_de_preferencia
                    ))
        
        # Commit the transaction
        connection.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()


