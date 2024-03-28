import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("IMGUR_API_KEY")
url = "https://api.imgur.com/3/image"

def is_valid_image_url(url):
    valid_extensions = ['.png', '.jpg', '.jpeg']
    for ext in valid_extensions:
        if url.endswith(ext):
            return True
    return False

def upload_image(image_url):
    payload = {"image": image_url}
    headers = {"Authorization": api_key}
    response = requests.request("POST", url, headers=headers, data=payload, files=[])
    print(response.json())
    return response.json().get("data").get("link")