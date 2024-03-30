import json
import os
import re
import time
import zipfile
from typing import List, Tuple, Dict
from tkinter import filedialog

from imgur import is_valid_image_url
from webdriver_actions import build_driver, get_details
from zip_archive_verification import has_cf_export_structure

# ------------- #

current_dir: str = os.path.dirname(os.path.abspath(__file__))
data_dir: str = os.path.join(current_dir, "..", "data")
data_path: str = os.path.join(data_dir, "data.json")
aux_img_data_path: str = os.path.join(data_dir, "aux_img_data.json")

home_dir: str = os.path.expanduser("~")

file_path: str = filedialog.askopenfilename(
    initialdir=home_dir, filetypes=[("Zip Files", "*.zip")]
)

archive: zipfile.ZipFile = zipfile.ZipFile(file_path)
if not has_cf_export_structure(archive):
    print("The selected archive does not have the correct structure for a CF export.")
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
    print(len(lines), len(file_triplets))
    print(
        "The number of files in the manifest does not match the number of files in the modlist."
    )
    exit()

# ------------- #

driver = build_driver()

# ------------- #

if os.path.exists(data_path):
    with open(data_path, "r") as file:
        if os.path.getsize(data_path) == 0:
            data: Dict = {}
        else:
            data = json.load(file)
else:
    data = {}
    with open(data_path, "w") as file:
        json.dump(data, file)

if os.path.exists(aux_img_data_path):
    with open(aux_img_data_path, "r") as file:
        if os.path.getsize(aux_img_data_path) == 0:
            aux_img_data: Dict[str, str] = {}
        else:
            aux_img_data = json.load(file)
else:
    aux_img_data = {}
    with open(aux_img_data_path, "w") as file:
        json.dump(aux_img_data, file)

# ------------- #
time_date_format: str = "%Y-%m-%d"
pattern: re.Pattern[str] = re.compile(r'<a href="(.*?)">(.*?) \(by (.*?)\)</a>')
for count, line in enumerate(lines):
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
        print(count, download_link)
        driver.get(download_link)
        page = driver.page_source
        project_details = get_details(page)
        if not project_details:
            print("Dead Link:", download_link)
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
            data[project_id]["last_updated"] = time.strftime(time_date_format)
            data[project_id]["versions"][file_id] = {
                "download_link": download_link,
                "file_name": file_name,
                "game_version": game_version,
            }

    if count % 10 == 0 or count == len(lines) - 1:
        with open(data_path, "w") as file:
            json.dump(data, file, indent=4)

        with open(aux_img_data_path, "w") as file:
            json.dump(aux_img_data, file, indent=4)

# ------------- #

driver.quit()
