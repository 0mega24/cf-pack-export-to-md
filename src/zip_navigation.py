"""_summary_"""

import zipfile
import os

def has_cf_export_structure(archive):
    file_names = set(["manifest.json", "modlist.html"])
    found_files = set()
    
    for file_info in archive.infolist():
        file_path = file_info.filename
        if not os.path.basename(file_path) in file_names:
            continue
        found_files.add(os.path.basename(file_path))
    
    return len(found_files) >= 2

archive = zipfile.ZipFile(input(), "r")
for file_info in archive.infolist():
    if "/" not in file_info.filename:
        print(file_info.filename)

