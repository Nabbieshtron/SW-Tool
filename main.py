import pygame
import pathlib
import json

from app import App
from main_menu import MainMenu
from rune import Rune
from settings import Settings
from constants import DEFAULT_PREFERENCES

# Paths
preferences_path = pathlib.Path().absolute() / "settings.json"
rune_path = pathlib.Path().absolute() / "runes.json"
persist = {}

if not rune_path.exists():
    rune_path.touch(exist_ok=True)
if not preferences_path.exists():
    preferences_path.touch(exist_ok=True)
    
# All this move to App class -> load from disk
with open(rune_path, "r") as file:
    try:
        persist['runes'] = json.load(file)
    except json.JSONDecodeError:
        persist['runes'] = {}

with open(preferences_path, "r+") as file:
    try:
        persist = json.load(file)
    except json.JSONDecodeError:
        json.dump(DEFAULT_PREFERENCES, file, indent=4)
        persist = DEFAULT_PREFERENCES

_app = App('Sw Tool', pygame.Rect(0, 0, 100, 100), 60)
main_menu = MainMenu(_app, persist, preferences_path)
rune = Rune(_app, persist, rune_path)
settings = Settings(_app, persist, preferences_path)

_app.run('main_menu', {'main_menu':main_menu, 'start':rune, 'settings':settings})