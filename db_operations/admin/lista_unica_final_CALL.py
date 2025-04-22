import requests
from datetime import datetime, timedelta
import os
from config import db_config, CLIENT_ID, CLIENT_SECRET, AUTH_URL, REQUESTS_CA_BUNDLE
from db_operations.admin.lista_unica_info import insert_data_to_db

access_token = None
token_expiry = None
os.environ["REQUESTS_CA_BUNDLE"] = REQUESTS_CA_BUNDLE

def get_access_token():
    global access_token, token_expiry
    try:
        if access_token and token_expiry > datetime.now():
            return access_token

        auth_payload = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
        auth_headers = {"Content-Type": "application/json"}
        auth_response = requests.post(AUTH_URL, json=auth_payload, headers=auth_headers)

        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            access_token = auth_data.get("Acess_Token")
            expiry_in_seconds = auth_data.get("expires_in", 3600)
            token_expiry = datetime.now() + timedelta(seconds=expiry_in_seconds)
            return access_token
        else:
            print(f"Auth failed: {auth_response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_data_with_token(oferta_num):
    token = get_access_token()
    if not token:
        print("Invalid token")
        return None
    try:
        formatted_url = f"https://outsysqa.azores.gov.pt/BEPA_Services_BL/rest/BolsaIlhas/CandidatoBolsaIlhasV2?Acess_Token={token}&OfertaNumber={oferta_num}"
        headers = {"Content-Type": "application/json"}
        response = requests.get(formatted_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            insert_data_to_db(data, db_config)
            return {"status": "success", "data": data}
        else:
            return {"status": "error", "details": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}