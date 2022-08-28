import json

def read_in(path: str) -> dict:

    with open(path, 'rb') as path:
        data = json.load(path)

    return data