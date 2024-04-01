import os
import time
import json
import requests
from typing import Dict, List
from dotenv import load_dotenv

from fileio import load_or_create_data

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

def main() -> None:
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    data_dir: str = os.path.join(current_dir, "..", "data")
    data_path: str = os.path.join(data_dir, "data.json")
    aux_img_data_path: str = os.path.join(data_dir, "aux_img_data.json")

    while True:
        start_time = time.time()
        data: Dict[str, Dict[str, str]] = load_or_create_data(data_path, {})
        aux_img_data: Dict[str, str] = load_or_create_data(aux_img_data_path, {})

        count = 0
        for key, value in aux_img_data.items():
            if data[key]["imgur_link"] == "":
                print(f"Uploading image {key}...")
                imgur_link: str = upload_image(value)
                data.setdefault(key, {})["imgur_link"] = imgur_link
                count += 1

                if count >= 50:
                    break

        with open(data_path, 'w') as file:
            json.dump(data, file,  indent=4)

        elapsed_time = time.time() - start_time
        time_to_sleep = max(0, 3600 - elapsed_time)
        time.sleep(time_to_sleep)

if __name__ == "__main__":
    main()
