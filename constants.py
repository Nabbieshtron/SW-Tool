from pygame import font, Rect
from button import Button

# Font
font.init()
BUTTON_FONT = font.SysFont("Arial", 30)
RUNE_QUALITY_FONT = font.SysFont("Arial", 30, True)
SETTINGS_FONT = font.SysFont("Arial", 30, True)
IN_APP_FONT = font.SysFont("Arial", 35)
RUNE_QUALITY_FONT = font.SysFont("Arial", 30, True)
BUTTON_FONT = font.SysFont("Arial", 30)
TEXT_BOX_FONT = font.SysFont("Arial Black", 36)

# Color
BACKGROUND_COLOR: tuple[int] = (168, 148, 95)
NAVIGATION_RECTANGLE_COLOR: tuple[int] = (153, 109, 38)
IN_APP_BG_COLOR: tuple[int] = (37, 24, 15)
IN_APP_TEXT_COLOR: tuple[int] = (182, 165, 112)
BUTTON_HOVER_COLOR = "#D74B4B"
BUTTON_BG_COLORS = ["#475F77", "#354B5E"]
BUTTON_TEXT_COLOR = "#FFFFFF"
TEXT_BOX_BORDER_COLORS = ['gray15', 'lightskyblue3']

# Button top part elevation height
ELEVATION: int = 6

BUTTON_TEXTS: dict = {
    "start": "Start",
    "settings": "Settings",
    "exit": "Exit",
    "assets": "Rune",
    "navigation_boxes": "True",
    "efficiency_default_value": "True",
    "save": "Save",
    "apply": "Apply",
    "cancel": "Cancel",
}
BUTTON_RECTS: dict = {
    "start": Rect(5, 16, 100, 35),
    "settings": Rect(5, 70, 100, 35),
    "exit": Rect(5, 125, 100, 35),
    "assets": Rect(400, 20, 150, 35),
    "navigation_boxes": Rect(400, 80, 150, 35),
    "efficiency_default_value": Rect(400, 140, 150, 35),
    "save": Rect(15, 450, 100, 35),
    "apply": Rect(325, 650, 150, 35),
    "cancel": Rect(525, 650, 150, 35),
}

# Navigation rectangles at the main menu interface
NAVIGATION_RECTANGLES_RECT = {
    "title": Rect(170, 20, 360, 50),
    "main": Rect(210, 0, 200, 50),
    "innate": Rect(210, 0, 200, 45),
    "substats": Rect(120, 0, 200, 130),
    "grade": Rect(447, 0, 130, 30),
}

# Display sizes
DISPLAY_SIZES: dict[str, tuple[int,int]] = {
    'main_menu': (600, 360),
    'settings': (1000, 700),
    'start': (600, 600),
    'artifact': (900, 400),
}
# Default values of min-max sub stat
DEFAULT_SUB_VALUES = {
    "cri_rate": [4, 6],
    "cri_dmg": [4, 7],
    "atk": [5, 8],
    "hp": [5, 8],
    "def": [5, 8],
    "resistance": [4, 8],
    "accuracy": [4, 8],
    "flat_spd": [4, 6],
    "flat_atk": [10, 20],
    "flat_def": [10, 20],
    "flat_hp": [135, 375],
}

# Default 5,6 star default value, increment value, max value
DEFAULT_MAIN_POWER_UP: dict = {
    "cri_rate": ([5, 7], [2.45, 3], [47, 58]),
    "cri_dmg": ([8, 11], [3.33, 4], [65, 80]),
    "atk": ([8, 11], [2.5, 3], [51, 63]),
    "hp": ([8, 11], [2.5, 3], [51, 63]),
    "def": ([8, 11], [2.5, 3], [51, 63]),
    "resistance": ([9, 12], [2.45, 3], [51, 64]),
    "accuracy": ([9, 12], [2.45, 3], [51, 64]),
    "flat_spd": ([5, 7], [2, 2], [39, 42]),
    "flat_atk": ([15, 22], [7, 8], [135, 160]),
    "flat_def": ([15, 22], [7, 8], [135, 160]),
    "flat_hp": ([270, 360], [105, 120], [2088, 2448]),
}

# In app
IN_APP_GRID = {
    "level": Rect(0, 150, 70, 70),
    "slot": Rect(0, 218, 70, 70),
    "rune_efficiency": Rect(0, 286, 70, 70),
    "none": Rect(0, 354, 70, 70),
    "grade": Rect(0, 112, 398, 40),
    "substats_grade": Rect(396, 112, 204, 40),
    "grinds": Rect(396, 150, 104, 274),
    "roll_efficiency": Rect(498, 150, 102, 274),
}

# Rune quality
RUNE_QUALITY_TEXT_COLORS: dict = {
    "magic": (223, 242, 135),
    "rare": (185, 254, 255),
    "hero": (255, 213, 244),
    "legend": (255, 178, 72),
}
RUNE_QUALITY_BG_COLORS: dict = {
    "magic": (30, 63, 6),
    "rare": (7, 66, 74),
    "hero": (92, 19, 65),
    "legend": (115, 50, 20),
}
RUNE_QUALITY: dict = {
    key: RUNE_QUALITY_FONT.render(key.capitalize(), True, RUNE_QUALITY_TEXT_COLORS[key])
    for key in ("magic", "rare", "hero", "legend")
}

RUNE_SETS = [
    "energy",
    "guard",
    "endure",
    "blade",
    "fatal",
    "swift",
    "despair",
    "rage",
    "focus",
    "vampire",
    "violent",
    "nemesis",
    "will",
    "shield",
    "revenge",
    "destroy",
    "fight",
    "determination",
    "enchance",
    "accuracy",
    "tolerance",
]

DEFAULT_PREFERENCES = {
    'assets_state': 'Rune',
    'navigation_boxes_state': True,
    'efficiency_default_value': True,
    'efficiency_multipliers': {
        'flat_hp': '0.5',
        'flat_def': '0.5',
        'flat_atk': '0.5',
        'hp': '1.0',
        'def': '1.0',
        'atk': '1.0',
        'flat_spd': '1.0',
        'cri_rate': '1.0',
        'cri_damage': '1.0',
        'accuracy': '1.0',
        'resistance': '1.0',
    },
    'transparent_dim': '',
}
        
# SETTINGS -> TEXTS WITH POSITIONS
SETTINGS_TEXTS_WITH_POS = (
    (Rect(20, 15, 0, 0), "Assets"),
    (Rect(20, 75, 0, 0), "Naviagtion boxes"),
    (Rect(20, 135, 0, 0), "Efficiency default value"),
    (Rect(650, 20, 0, 0), "Efficiency multipliers"),
    (Rect(650, 75, 0, 0), "HP flat"),
    (Rect(650, 125, 0, 0), "DEF flat"),
    (Rect(650, 175, 0, 0), "ATK flat"),
    (Rect(650, 225, 0, 0), "HP"),
    (Rect(650, 275, 0, 0), "DEF"),
    (Rect(650, 325, 0, 0), "ATK"),
    (Rect(650, 375, 0, 0), "SPD"),
    (Rect(650, 425, 0, 0), "CRI Rate"),
    (Rect(650, 475, 0, 0), "CRI Damage"),
    (Rect(650, 525, 0, 0), "Accuracy"),
    (Rect(650, 575, 0, 0), "Resistance"),
)

DEFAULT_EFFICIENCY_MULTIPLIER = {
    "flat_hp": '0.5',
    "flat_def": '0.5',
    "flat_atk": '0.5',
    "hp": '1.0',
    "def": '1.0',
    "atk": '1.0',
    "flat_spd": '1.0',
    "cri_rate": '1.0',
    "cri_damage": '1.0',
    "accuracy": '1.0',
    "resistance": '1.0',
}

EFFICIENCY_MULTIPLIERS_TEXT_BOXES_ATTRIBUTES = [(850, 75+(50*n), 100, 40) for n in range(0, 11)]

