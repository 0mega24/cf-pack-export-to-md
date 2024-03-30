import requests
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

api_key: str = os.getenv("IMGUR_API_KEY")
url: str = "https://api.imgur.com/3/image"


def is_valid_image_url(url: str) -> bool:
    valid_extensions: List[str] = [".png", ".jpg", ".jpeg"]
    for ext in valid_extensions:
        if url.endswith(ext):
            return True
    return False


def upload_image(image_url: str) -> str:
    payload: dict = {"image": image_url}
    headers: dict = {"Authorization": api_key}
    response: requests.Response = requests.request(
        "POST", url, headers=headers, data=payload, files=[]
    )
    print(response.json())
    return str(response.json().get("data").get("link"))
