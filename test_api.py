import requests
import time
import os
from datetime import datetime, timedelta
from config import db_config,CLIENT_ID,CLIENT_SECRET,AUTH_URL,REQUESTS_CA_BUNDLE
from db_operations.admin.api_info import insert_data_to_db 


access_token = None
token_expiry = None
os.environ["REQUESTS_CA_BUNDLE"] = REQUESTS_CA_BUNDLE

def get_access_token():
    
    global access_token, token_expiry
    
    try:
        if access_token and token_expiry > datetime.now():
            print("Using existing access token.")
            return access_token

        auth_payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        auth_headers = {
            "Content-Type": "application/json"
        }
 
        auth_response = requests.post(AUTH_URL, json=auth_payload, headers=auth_headers)
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            access_token = auth_data.get("Acess_Token")
            if not access_token:
                print("Access token not found in the authentication response.")
                return None
            
            expiry_in_seconds = auth_data.get("expires_in", 3600)  # Default expiry time of 1 hour
            token_expiry = datetime.now() + timedelta(seconds=expiry_in_seconds)
            print(f"New access token acquired. Expiry: {token_expiry}")
            return access_token
        else:
            print(f"Authentication failed. Status code: {auth_response.status_code}")
            print(f"Details: {auth_response.text}")
            return None
    
    except Exception as e:
        print(f"Error while fetching access token: {str(e)}")
        return None


def fetch_data_with_token(token):
    
    if not token:
        print("Invalid token, unable to fetch data.")
        return

    try:
        # Format the URL with the token
        formatted_url = f"https://outsysqa.azores.gov.pt/BEPA_Services_BL/rest/BolsaIlhas/CandidatoBolsaIlhasV2?Acess_Token={token}&OfertaNumber=56%2F2025"
        
        # Set the headers for the GET request
        headers = {
            "Content-Type": "application/json"
        }
        
        # Send the GET request
        response = requests.get(formatted_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON data from the response
            print("entrei ca dentro")
            data = response.json()
            print(data)
            # Insert the data into the database
            insert_data_to_db(data, db_config)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(f"Details: {response.text}")
    
    except Exception as e:
        print(f"Error while fetching data: {str(e)}")
        
def main():
    while True:
        # Step 1: Get the access token (either reuse or refresh)
        token = get_access_token()
        if token:
            print(f"Access Token: {token}")
            # Step 2: Fetch data using the token
            fetch_data_with_token(token)
        else:
            print("Could not retrieve access token. Exiting.")
        
        # Wait for 30 minutes before the next run
        time.sleep(1800)  


# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    main()