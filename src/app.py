import os
import re
import json
import time
import logging
import zipfile
import argparse
from tqdm import tqdm
from tkinter import filedialog
from typing import List, Tuple, Dict

from imgur import is_valid_image_url
from webdriver_actions import build_driver, get_details
from zip_archive_verification import has_cf_export_structure

# ------------- #

def load_or_create_data(file_path: str, default_dict: Dict) -> Dict:
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            if os.path.getsize(file_path) == 0:
                data = default_dict
            else:
                data = json.load(file)
    else:
        data = default_dict
        with open(file_path, "w") as file:
            json.dump(data, file)
    return data

# ------------- #

parser = argparse.ArgumentParser()
parser.add_argument(
    "--log",
    default="WARNING",
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help="Minimum logging level to display (default: INFO)",
)
args = parser.parse_args()

# ------------- #

logging.basicConfig(
    level=args.log, filename="logfile.log", format="%(levelname)s: %(message)s"
)

# ------------- #

current_dir: str = os.path.dirname(os.path.abspath(__file__))
data_dir: str = os.path.join(current_dir, "..", "data")
data_path: str = os.path.join(data_dir, "data.json")
aux_img_data_path: str = os.path.join(data_dir, "aux_img_data.json")

home_dir: str = os.path.expanduser("~")

# ------------- #

file_path: str = filedialog.askopenfilename(
    initialdir=home_dir, filetypes=[("Zip Files", "*.zip")]
)

archive: zipfile.ZipFile = zipfile.ZipFile(file_path)
if not has_cf_export_structure(archive):
    logging.fatal(
        "The selected archive does not have the correct structure for a CF export."
    )
    exit()

# ------------- #

lines: List[bytes] = []
with archive.open("modlist.html") as modlist:
    lines = modlist.readlines()
lines = lines[1:-1]

file_triplets: List[Tuple[int, int, bool]] = []
with archive.open("manifest.json") as manifest:
    manifest = json.load(manifest)
    file_triplets = [
        (file["projectID"], file["fileID"], file["required"])
        for file in manifest["files"]
    ]

if len(lines) != len(file_triplets):
    logging.fatal(
        "The number of files in the manifest does not match the number of files in the modlist."
    )
    exit()

# ------------- #

data: Dict = load_or_create_data(data_path, {})
aux_img_data: Dict = load_or_create_data(aux_img_data_path, {})

# ------------- #

driver = build_driver()

# ------------- #

time_date_format: str = "%Y-%m-%d"
pattern: re.Pattern[str] = re.compile(r'<a href="(.*?)">(.*?) \(by (.*?)\)</a>')
for count, line in enumerate(tqdm(lines, desc="Processing", unit="links")):
    match = pattern.search(line.decode("utf-8"))

    link: str = match.group(1)
    name: str = match.group(2)
    author: str = match.group(3)
    project_id: str = str(file_triplets[count][0])
    file_id: str = str(file_triplets[count][1])
    download_link: str = f"{link}/files/{file_id}"

    missing_project: bool = project_id not in data.keys()
    if not missing_project:
        missing_file: bool = file_id not in data[project_id]["versions"].keys()
    else:
        missing_file = False

    if missing_project or missing_file:
        driver.get(download_link)
        page = driver.page_source
        project_details = get_details(page)
        if not project_details:
            logging.warning(f"Dead Link: {download_link}")
            link = ""
            download_link = ""
            project_details = ["", "", "", "", "", "", ""]

        description: str = project_details[0]
        total_downloads: str = project_details[1]
        img_src: str = project_details[2]
        file_name: str = project_details[3]
        game_version: str = project_details[4]
        license: str = project_details[5]

        if missing_project:
            logging.info(f"Adding New Project: {name}")
            if is_valid_image_url(img_src):
                aux_img_data[project_id] = img_src
            data[project_id] = {
                "name": name,
                "author": author,
                "description": description,
                "total_downloads": total_downloads,
                "license": license,
                "project_link": link,
                "img_src": img_src,
                "imgur_link": "",
                "last_updated": time.strftime(time_date_format),
                "versions": {
                    file_id: {
                        "download_link": download_link,
                        "file_name": file_name,
                        "game_version": game_version,
                    }
                },
            }
        elif missing_file:
            logging.info(f"Adding File: {file_id}")
            data[project_id]["last_updated"] = time.strftime(time_date_format)
            data[project_id]["versions"][file_id] = {
                "download_link": download_link,
                "file_name": file_name,
                "game_version": game_version,
            }

    if count % 10 == 0 or count == len(lines) - 1:
        logging.debug(f"Saving Data Up To Number: {count}")
        with open(data_path, "w") as file:
            json.dump(data, file, indent=4)

        with open(aux_img_data_path, "w") as file:
            json.dump(aux_img_data, file, indent=4)

# ------------- #

driver.quit()
