"""
This module contains a function for extracting information from 
modlist.html and manifest.json files in an input archive.

The function `prescrape` takes an input archive as a parameter and returns 
a dictionary containing formatted data extracted from the files.

The dictionary contains information about each mod, including its 
name, author, link, download link, project ID, file ID, and whether it is required or not.

Example usage:
    import zipfile

    input_archive = zipfile.ZipFile("archive.zip")
    formatted_data = prescrape(input_archive)
    print(formatted_data)
"""

import json
import re
import zipfile


def prescrape(input_archive: zipfile.ZipFile) -> list[dict]:
    """
    Extracts information from modlist.html and manifest.json files in the input archive.

    Args:
        input_archive (zipfile.ZipFile): 
        The input archive containing modlist.html and manifest.json files.

    Returns:
        list[dict]: A dictionary containing formatted data extracted from the files.
            Each entry in the dictionary represents a mod 
            and includes the following information:
            - name: The name of the mod.
            - author: The author of the mod.
            - link: The link to the mod.
            - downloadlink: The download link for the mod.
            - projectID: The project ID of the mod.
            - fileID: The file ID of the mod.
            - required: Whether the mod is required or not.
    """
    pattern = re.compile(r'<a href="(.*?)">(.*?) \(by (.*?)\)</a>')
    lines = []
    with input_archive.open("modlist.html") as modlist:
        lines = modlist.readlines()
    lines = lines[1:-1]

    file_triplets = []
    with input_archive.open("manifest.json") as manifest:
        manifest = json.load(manifest)
        file_triplets = [
            (file["projectID"], file["fileID"], file["required"])
            for file in manifest["files"]
        ]

    formatted_data = []

    for count, line in enumerate(lines):
        line = line.decode("utf-8")
        match = pattern.search(line)
        link = match.group(1)
        name = match.group(2)
        author = match.group(3)
        project_id = file_triplets[count][0]
        file_id = file_triplets[count][1]
        required = file_triplets[count][2]
        download_link = f"{link}/files/{file_id}"
        formatted_data.append(
            {
            "projectID": project_id,
            "name": name,
            "author": author,
            "link": link,
            "fileID": file_id,
            "downloadlink": download_link,
            "required": required
            }
        )
    return formatted_data
