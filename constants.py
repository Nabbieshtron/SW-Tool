from pygame import font
from pygame.locals import Rect

# Initalize font
font.init()

# Fonts
BUTTON_FONT = font.SysFont("Arial", 30)
RUNE_QUALITY_FONT = font.SysFont("Arial", 30, True)
SETTINGS_FONT = font.SysFont("Arial", 30, True)
IN_APP_FONT = font.SysFont("Arial", 35)

# Colors
# Main menu color
BG_COLOR: tuple[int] = (168, 148, 95)
# In app bg color, Set - > bg color
IN_APP_BG_COLOR: tuple[int] = (37, 24, 15)
IN_APP_TEXT_COLOR: tuple[int] = (182, 165, 112)
# Transperancy color for the hole in the app
TRANSPARENCY_COLOR: tuple[int] = (255, 0, 128)
# Main menu - > border color for the 4 rectangles in the tranparent section
MENU_BORDER_COLOR: tuple[int] = (153, 109, 38)
# Button colors
BUTTON_EFFECT_ON_COLOR: str = "#D74B4B"
BUTTON_EFFECT_OFF_COLOR: str = "#475F77"
BUTTON_BOTTOM_COLOR: str = "#354B5E"
BUTTON_TEXT_COLOR: str = "#FFFFFF"

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

DEFAULT_RUNE_QUALITY: dict = {
    "magic": RUNE_QUALITY_FONT.render("Magic", True, RUNE_QUALITY_TEXT_COLORS["magic"]),
    "rare": RUNE_QUALITY_FONT.render("Rare", True, RUNE_QUALITY_TEXT_COLORS["rare"]),
    "hero": RUNE_QUALITY_FONT.render("Hero", True, RUNE_QUALITY_TEXT_COLORS["hero"]),
    "legend": RUNE_QUALITY_FONT.render(
        "Legend", True, RUNE_QUALITY_TEXT_COLORS["legend"]
    ),
}

# Buttons core
ELEVATION: int = 6
# Width
BUTTON_WIDTH: dict = {"menu": 100, "settings": 150}
# Height
BUTTON_HEIGHT: dict = {"menu": 35, "settings": 35}
# Size
BUTTON_SIZE: dict = {
    key: (BUTTON_WIDTH[key], BUTTON_HEIGHT[key]) for key in ("menu", "settings")
}

# Buttons names
BUTTON_NAMES: dict = {
    "set": "Set",
    "settings": "Settings",
    "exit": "Exit",
    "asset_type": "Rune",
    "hide_or_show": "Show",
    "apply_changes": "Apply",
    "cancel_changes": "Cancel",
}

# Button positions key:value (pos_x, pos_y)
BUTTON_POSITIONS: dict = {
    "set": (5, 16),
    "settings": (5, 70),
    "exit": (5, 125),
    "asset_type": (400, 15),
    "hide_or_show": (400, 75),
    "apply_changes": (140, 550),
    "cancel_changes": (310, 550),
}

# Rune box position, size in the main_menu
RUNE_RECTS: dict = {
    "title_rect": Rect(170, 20, 360, 50),
    "main_rect": Rect(210, 0, 200, 50),
    "inate_rect": Rect(210, 0, 200, 45),
    "sub_rect": Rect(120, 0, 200, 130),
}

# Arifact box position, size in the main_menu
ARTIFACT_RECTS: dict = {
    "title_rect": Rect(170, 20, 360, 50),
    "main_rect": Rect(210, 0, 150, 50),
    "inate_rect": Rect(210, 0, 200, 45),
    "sub_rect": Rect(120, 0, 330, 140),
}

# Default values of min-max sub stat
DEFAULT_SUB_VALUES: dict = {
    "no_flat": {
        "cri rate": [4, 6],
        "cri dmg": [4, 7],
        "atk": [5, 8],
        "hp": [5, 8],
        "def": [5, 8],
        "resistance": [4, 8],
        "accuracy": [4, 8],
    },
    "flat": {
        "spd": [4, 6],
        "atk": [10, 20],
        "def": [10, 20],
        "hp": [135, 375],
    },
}

DEFAULT_MAIN_POWER_UP: dict = {
    "no_flat": {
        "cri rate": ([5, 7], [2.45, 3], [47, 58]),
        "cri dmg": ([8, 11], [3.33, 4], [65, 80]),
        "atk": ([8, 11], [2.45, 3], [51, 63]),
        "hp": ([8, 11], [2.45, 3], [51, 63]),
        "def": ([8, 11], [2.45, 3], [51, 63]),
        "resistance": ([9, 12], [2.45, 3], [51, 64]),
        "accuracy": ([9, 12], [2.45, 3], [51, 64]),
    },
    "flat": {
        "spd": ([5, 7], [2, 2], [39, 42]),
        "atk": ([15, 22], [7, 8], [135, 160]),
        "def": ([15, 22], [7, 8], [135, 160]),
        "hp": ([270, 360], [105, 120], [2088, 2448]),
    },
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

DEFAULT_SYNERGY_SET_SUBS = {
    "quality": ["spd", "hp", "def", "atk", "accuracy", "resistance", "cri rate"],
    "damage": ["spd", "cri rate", "cri dmg", "atk"],
}

DEFAULT_SYNERGY_SLOT = {"quality": {"1": 1}}

# Settings rendered text
SETTINGS_TEXT_SURFACES: dict = {
    "assets": SETTINGS_FONT.render("Select game asset", True, "Black"),
    "navsquares": SETTINGS_FONT.render("Navigation squares", True, "Black"),
}

SETTINGS_TEXT_RECTS: dict = {
    "assets": SETTINGS_TEXT_SURFACES["assets"].get_rect(topleft=(20, 20)),
    "navsquares": SETTINGS_TEXT_SURFACES["navsquares"].get_rect(topleft=(20, 80)),
}

IN_APP_GRID = {
    "level": Rect(0, 150, 70, 70),
    "slot": Rect(0, 218, 70, 70),
    "rune_eff": Rect(0, 286, 70, 70),
    "none": Rect(0, 354, 70, 70),
    "el_grade": Rect(0, 112, 198, 40),
    "eh_grade": Rect(196, 112, 202, 40),
    "sub_grade": Rect(396, 112, 204, 40),
    "grinds": Rect(396, 150, 104, 274),
    "roll_eff": Rect(498, 150, 102, 274),
}

# Display size
DISPLAY_MAIN_MENU: tuple[int] = 600, 360
DISPLAY_SETTINGS: tuple[int] = 600, 600
DISPLAY_RUNE: tuple[int] = 600, 600
DISPLAY_ARTIFACT: tuple[int] = 900, 400
