import pygame
import pathlib
import json

import user_config
from app import App
from main_menu import MainMenu
from rune_manager import RuneManager
from grind_manager import GrindManager
from settings import Settings

_app = App('Sw Tool', pygame.Rect(0, 0, 100, 100), 60)

# Paths
config_path = pathlib.Path().absolute() / "settings.json"
rune_path = pathlib.Path().absolute() / "runes.json"
grind_path = pathlib.Path().absolute() / "grind.json"

# Loading save data
persist = {}
persist['runes'] = user_config.load_runes(rune_path)
persist.update(user_config.load_settings(config_path))
main_menu = MainMenu(_app, persist, config_path)
rune_manager = RuneManager(_app, persist, rune_path)
grind_manager = GrindManager(_app, persist, grind_path)
settings = Settings(_app, persist, config_path)

_app.run('main_menu', {
    'main_menu':main_menu, 
    'settings':settings, 
    'rune_manager':rune_manager,
    'grind_manager':grind_manager,
    }
)