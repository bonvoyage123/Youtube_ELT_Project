import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:\\Python_Code\\Youtube_ELT_Project\\.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")

def get_playlist_id():
    try:
        URL= f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        print(f"API_KEY loaded: {API_KEY}")
        response = requests.get(URL)

        #Python object to JSON string
        data = response.json()

        #Readable format for JSON  {Optional}
        #print(json.dumps(data, indent=4))
        
        channel_items = data['items'][0]
        channel_upload_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(channel_upload_id) 
        
        return channel_upload_id
    
    except requests.exceptions.RequestException as e:
        raise e
    

def get_video_ids(playlist_id):
    try:
        video_ids = []
        page_token = None
        base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}"

        while True:
            url = base_url
            if page_token:
                url += f"&pageToken={page_token}" # If page_token exists, add it to the URL for pagination. Variable in the URL needs a, '&' prefix.
            response = requests.get(url)
            response.raise_for_status() # To highlight 404 or 500 errors -> HTTPS Errors
            data = response.json()
        
        # Now we will extract video IDs from the response data and handle pagination until there are no more pages left        
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_token = data.get('nextPageToken')

            if not page_token:
                break
        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    print(video_ids)
    print(f"Total videos: {len(video_ids)}")