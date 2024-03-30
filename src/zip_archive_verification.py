import zipfile
import os
from typing import Set


def has_cf_export_structure(input_archive: zipfile.ZipFile) -> bool:
    file_names: Set[str] = {"manifest.json", "modlist.html"}
    found_files: Set[str] = {
        os.path.basename(file_info.filename) for file_info in input_archive.infolist()
    }
    return file_names.issubset(found_files)
