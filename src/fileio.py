import os
import json
from typing import Dict


def load_or_create_data(file_path: str, default_dict: Dict) -> Dict:
    """
    Load data from a JSON file if it exists, otherwise create and initialize with a default dictionary.

    Args:
        file_path (str): Path to the JSON file.
        default_dict (Dict): Default dictionary to initialize with if the file doesn't exist.

    Returns:
        Dict: Loaded or newly created dictionary.
    """
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