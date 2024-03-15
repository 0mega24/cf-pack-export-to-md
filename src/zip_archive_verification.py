"""
This module provides functions for verifying the structure of a zip archive.

The main function in this module is `has_cf_export_structure`, which checks if the input archive
has the required structure for a CF export. It takes a `zipfile.ZipFile` object as input and returns
a boolean value indicating whether the archive has the required structure.

Example usage:
    import zipfile
    import zip_archive_verification

    archive = zipfile.ZipFile("path/to/archive.zip")
    if zip_archive_verification.has_cf_export_structure(archive):
        print("The archive has the required structure.")
    else:
        print("The archive does not have the required structure.")
"""

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
