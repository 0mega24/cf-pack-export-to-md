import zipfile
import os


def has_cf_export_structure(input_archive: zipfile.ZipFile) -> bool:
    """
    Check if the input archive has the required structure for a CF export.

    Args:
        input_archive (zipfile.ZipFile): The input archive to be checked.

    Returns:
        bool: True if the archive has the required structure, False otherwise.
    """
    file_names = {"manifest.json", "modlist.html"}
    found_files = {
        os.path.basename(file_info.filename) for file_info in input_archive.infolist()
    }
    return file_names.issubset(found_files)
