import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:\\Python_Code\\Youtube_ELT_Project\\.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        URL= f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        print(f"API_KEY loaded: {API_KEY}")
        response = requests.get(URL)

        #Python object to JSON string
        data = response.json()

        #Readable format for JSON
        print(json.dumps(data, indent=4))
        
        if 'error' in data:
            print(f"\nAPI Error: {data['error']['message']}")
            return None
        
        if 'items' not in data:
            print("Error: 'items' not found in response")
            return None
        
        channel_items = data['items'][0]
        channel_upload_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(channel_upload_id)
        
        return channel_upload_id
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_playlist_id()