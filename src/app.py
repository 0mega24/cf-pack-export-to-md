"""
This script allows the user to select a zip file and checks 
if it has the correct structure for a CF export.
"""

import os
import zipfile
from tkinter import filedialog

from zip_archive_verification import has_cf_export_structure

home_dir = os.path.expanduser("~")
os.chdir(home_dir)

file_path = filedialog.askopenfilename(
    initialdir=home_dir, filetypes=[("Zip Files", "*.zip")]
)
print(file_path)
print(has_cf_export_structure(zipfile.ZipFile(file_path)))
