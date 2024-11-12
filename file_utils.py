import os
import json


def file_exists(filename):
    return os.path.isfile(filename)


def load_json(filepath):
    if not file_exists(filepath):
        raise FileNotFoundError(f'File "{filepath}" does not exist')
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
