"""
This script allows the user to select a zip file and checks
if it has the correct structure for a CF export.
"""

import json
import os
import re
import zipfile
from tkinter import filedialog

from webdriver_actions import build_driver
from zip_archive_verification import has_cf_export_structure

# ------------- #

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")
data_path = os.path.join(data_dir, "data.json")

home_dir = os.path.expanduser("~")

file_path = filedialog.askopenfilename(
    initialdir=home_dir, filetypes=[("Zip Files", "*.zip")]
)

archive = zipfile.ZipFile(file_path)
if not has_cf_export_structure(archive):
    print("The selected archive does not have the correct structure for a CF export.")
    exit()

# ------------- #

lines = []
with archive.open("modlist.html") as modlist:
    lines = modlist.readlines()
lines = lines[1:-1]

file_triplets = []
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
            data = {}
        else:
            data = json.load(file)
else:
    data = {}
    with open(data_path, "w") as file:
        json.dump(data, file)

# ------------- #

pattern = re.compile(r'<a href="(.*?)">(.*?) \(by (.*?)\)</a>')
for count, line in enumerate(lines):
    match = pattern.search(line.decode("utf-8"))
    link = match.group(1)
    name = match.group(2)
    author = match.group(3)
    project_id = file_triplets[count][0]
    file_id = file_triplets[count][1]
    download_link = f"{link}/files/{file_id}"
    
    

    if project_id not in data:
        pass  # TODO: scrape the project_link and download_link
    else:
        if file_id not in data[project_id]["versions"]:
            pass  # TODO: scrape just the download_link

    # data[project_id] = {}  # TODO: build dict structure to pass into json.dump

# ------------- #
