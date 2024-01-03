import json
from pygame import Rect
from rune import Rune
from constants import DEFAULT_CONFIGURATIONS

    
def save_settings(data, path):
    try:
        with open(path, "r") as file:
            loaded = json.load(file)
            loaded.update(data)
    except (json.JSONDecodeError, FileNotFoundError):
        loaded = data
    
    with open(path, 'w+') as file:
        json.dump(loaded, file, indent=4)
    
def load_settings(path) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        save(DEFAULT_CONFIGURATIONS, path)
        return DEFAULT_CONFIGURATIONS

def save_runes(data, path):
    if data is not None:  
        try:
            with open(path, "r") as file:
                loaded = json.load(file)
                loaded.update(data)
            
            with open(path, 'w+') as file:
                json.dump(loaded, file, indent=4)
                
        except (json.JSONDecodeError, FileNotFoundError):
            with open(path, 'w+') as file:
                json.dump(data, file, indent=4)
    else:
        print("Nothing to save")

def load_runes(path) -> dict:
    try:
        with open(path, "r") as file:
            loaded = json.load(file)
            return {id_: Rune.from_dict(rune) for id_, rune in loaded.items()}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}