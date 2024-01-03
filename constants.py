import pygame

from dataclasses import dataclass, field

# Initalizing pygame fonts
pygame.font.init()

SETTINGS_FONT = pygame.font.SysFont("Arial Black", 30, True)
START_FONT = pygame.font.SysFont("Consolas", 35)
TEXT_BOX_FONT = pygame.font.SysFont("Arial Black", 36)
GRIND_MANAGER_FONT = pygame.font.SysFont("Arial Black", 20)

# Color
BG_COLOR: tuple[int] = (168, 148, 95)
POSITION_INDICATOR_COLOR: str = "Red"
NAVIGATION_RECTANGLE_COLOR: tuple[int] = (153, 109, 38)
START_BG_COLOR: tuple[int] = (37, 24, 15)
START_TEXT_COLOR: tuple[int] = (182, 165, 112)
TEXT_BOX_COLOR = ('lightskyblue3','gray15')

def render(
    text:str, 
    font: pygame.font, 
    color, 
    position: tuple[int,int] = (0,0)
    ):
    surface = font.render(text, True, color)
    rect = surface.get_rect(topleft=(position[0], position[1]))
    return surface, rect

@dataclass(frozen=True)
class PowerUp:
    '''All the information about rune power uping'''
    name: str
    grade: int
    start: int
    increment: float
    end: int
    flat: bool = field(default=False)
    
@dataclass
class Quality:
    name: str
    color_text: tuple[int,int,int]
    color_fill: tuple[int,int,int]
    font: pygame.font = pygame.font.SysFont("Arial", 30, True)
    
    def __post_init__(self):
        self.surface, self.surface_rect = render(
            self.name, 
            self.font, 
            self.color_text,
            self.color_text
        )
  
MAIN_POWER_UP: dict = {
    "cri rate": (
        PowerUp(name='Critical rate', grade=5, start=5, increment=2.45, end=47),
        PowerUp(name='Critical rate', grade=6, start=7, increment=3.0, end=58),
    ),
    "cri dmg": (
        PowerUp(name='Critical damage', grade=5, start=8, increment=3.33, end=65),
        PowerUp(name='Critical damage', grade=6, start=11, increment=4, end=80),
    ),

    "atk": (
        PowerUp(name='Attack', grade=5, start=8, increment=2.5, end=51),
        PowerUp(name='Attack', grade=5, start=15, increment=7.0, end=135, flat=True),
        PowerUp(name='Attack', grade=6, start=11, increment=3.0, end=63),
        PowerUp(name='Attack', grade=6, start=22, increment=8.0, end=160, flat=True),
    ),

    "hp": (
        PowerUp(name='Health points', grade=5, start=8, increment=2.5, end=51),
        PowerUp(name='Health points', grade=5, start=270, increment=105.0, end=2088, flat=True),
        PowerUp(name='Health points', grade=6, start=11, increment=3.0, end=63),
        PowerUp(name='Health points', grade=6, start=360, increment=120.0, end=2448, flat=True),
    ),

    "def": (
        PowerUp(name='Defence', grade=5, start=8, increment=2.5, end=51),
        PowerUp(name='Defence', grade=5, start=15, increment=7.0, end=135, flat=True),
        PowerUp(name='Defence', grade=6, start=11, increment=3.0, end=63),
        PowerUp(name='Defence', grade=6, start=22, increment=8.0, end=160, flat=True),
    ),
    
    "resistance": (
        PowerUp(name='Resistance', grade=5, start=9, increment=2.45, end=51),
        PowerUp(name='Resistance', grade=6, start=12, increment=3.0, end=64),
    ),

    "accuracy": (
        PowerUp(name='Accuracy', grade=5, start=9, increment=2.45, end=51),
        PowerUp(name='Accuracy', grade=6, start=12, increment=3.0, end=64),
    ),

    "spd": (
        PowerUp(name='Speed', grade=5, start=5, increment=2.0, end=39, flat=True),
        PowerUp(name='Speed', grade=6, start=7, increment=2.0, end=42, flat=True),
    ),
}

RUNE_GRADES = {
    'magic': Quality(name='Magic', color_text=(223, 242, 135), color_fill=(30, 63, 6)),
    'rare': Quality(name='Rare', color_text=(185, 254, 255), color_fill=(7, 66, 74)),
    'hero': Quality(name='Hero', color_text=(255, 213, 244), color_fill=(92, 19, 65)),
    'legend': Quality(name='Legend', color_text=(255, 178, 72), color_fill=(115, 50, 20)),
}

RUNE_SETS = (
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
)

RUNE_SLOTS = tuple(str(n) for n in range(1,7))
RUNE_LEVEL = tuple(str(n) for n in range(1,16))

# Default values of min-max sub stat
SUB_VALUES = {
    "atk flat": (10, 20, True),
    "hp flat": (135, 375, True),
    "def flat":  (10, 20, True),
    "def": (5, 8, False),
    "hp": (5, 8, False),
    "atk": (5, 8, False),
    "cri rate": (4, 6, False),
    "cri dmg": (4, 7, False),
    "resistance": (4, 8, False),
    "accuracy": (4, 8, False),
    "spd": (4, 6, True),
}

# Navigation rectangles at the main menu interface
NAVIGATION_RECTANGLES_RECT = {
    "title": pygame.Rect(170, 20, 360, 50),
    "main": pygame.Rect(210, 0, 200, 50),
    "innate": pygame.Rect(210, 0, 200, 45),
    "substats": pygame.Rect(120, 0, 200, 130),
    "grade": pygame.Rect(447, 0, 130, 30),
}

# Display sizes
DISPLAY_SIZES: dict[str, tuple[int,int]] = {
    'main_menu': (600, 360),
    'settings': (1000, 700),
    'rune_manager': (1200, 650),
    'grind_manager': (1920, 1080),
    'artifact': (900, 400),
}

START_GRID = {
    "level": pygame.Rect(0, 150, 70, 70),
    "slot": pygame.Rect(0, 218, 70, 70),
    "efficiency": pygame.Rect(0, 286, 70, 70),
    "none": pygame.Rect(0, 354, 70, 70),
    "grade": pygame.Rect(0, 112, 398, 40),
    "substats_grade": pygame.Rect(396, 112, 204, 40),
    "grinds": pygame.Rect(396, 150, 104, 274),
    "roll_efficiency": pygame.Rect(498, 150, 102, 274),
}

DEFAULT_CONFIGURATIONS = {
    'assets': 'Rune',
    'navigation_boxes': True,
    'efficiency_default_value': True,
    'is_set': False,
    'efficiency_multipliers': {
        'hp flat': 0.5,
        'def flat': 0.5,
        'atk flat': 0.5,
        'hp': 1.0,
        'def': 1.0,
        'atk': 1.0,
        'spd': 1.0,
        'cri rate': 1.0,
        'cri dmg': 1.0,
        'accuracy': 1.0,
        'resistance': 1.0, 
    },
    "window_rect_attribute": None,
    "transparent_rect": None,
    "navigation_rect_attributes":  None,
}

SETTINGS_BLIT=(
    render(text="Assets", font=SETTINGS_FONT, color="Black", position=(20, 15)),
    render(text="Naviagtion boxes", font=SETTINGS_FONT, color="Black", position=(20, 75)),
    render(text="Efficiency default value", font=SETTINGS_FONT, color="Black", position=(20, 135)),
    render(text="Efficiency multipliers", font=SETTINGS_FONT, color="Black", position=(650, 20)),
    render(text="HP flat", font=SETTINGS_FONT, color="Black", position=(650, 75)),
    render(text="DEF flat", font=SETTINGS_FONT, color="Black", position=(650, 125)),
    render(text="ATK flat", font=SETTINGS_FONT, color="Black", position=(650, 175)),
    render(text="HP", font=SETTINGS_FONT, color="Black", position=(650, 225)),
    render(text="DEF", font=SETTINGS_FONT, color="Black", position=(650, 275)),
    render(text="ATK", font=SETTINGS_FONT, color="Black", position=(650, 325)),
    render(text="SPD", font=SETTINGS_FONT, color="Black", position=(650, 375)),
    render(text="CRI Rate", font=SETTINGS_FONT, color="Black", position=(650, 425)),
    render(text="CRI Damage", font=SETTINGS_FONT, color="Black", position=(650, 475)),
    render(text="Accuracy", font=SETTINGS_FONT, color="Black", position=(650, 525)),
    render(text="Resistance", font=SETTINGS_FONT, color="Black", position=(650, 575)),
)

'''
    def_sub_value, default substat value
    cur_sub_value, current substat value
    cur_grind_value, current grind value
    cur_gem_value, current gem value
    cur_sub_eff_value, current substat efficiency value
    w_sub_eff_value_after_gg, wanter substat efficiency value after grind and gems filled in w_grind_value or w_gem_value
    w_grind_value, wanted grind value
    w_gem_value, wanted gem value
    r_efficiency, rune efficiency
    rp_efficiency, rune max efficiency
'''
GRIND_MANAGER_RECTS = {
    'id': pygame.Rect(0, 0, 100, 40),
    'level': pygame.Rect(98, 0, 100, 40),
    'slot': pygame.Rect(196, 0, 100, 40),
    'set': pygame.Rect(294, 0, 200, 40),
    'main': pygame.Rect(492, 0, 200, 40),
    'innate': pygame.Rect(788, 0, 200, 40),
    'main_value': pygame.Rect(690, 0, 100, 40),
    'innate_value': pygame.Rect(986, 0, 100, 40),
    'r_efficiency': pygame.Rect(1084, 0, 100, 40),
    'rp_efficiency': pygame.Rect(1182, 0, 100, 40),
    'grind_menu_borders': pygame.Rect(0, 38, 1920, 260),
    'def_sub_value_1': pygame.Rect(240, 60, 100, 40),
    'def_sub_value_2': pygame.Rect(240, 120, 100, 40),
    'def_sub_value_3': pygame.Rect(240, 180, 100, 40),
    'def_sub_value_4': pygame.Rect(240, 240, 100, 40),
    'cur_sub_value_1': pygame.Rect(360, 60, 100, 40),
    'cur_sub_value_2': pygame.Rect(360, 120, 100, 40),
    'cur_sub_value_3': pygame.Rect(360, 180, 100, 40),
    'cur_sub_value_4': pygame.Rect(360, 240, 100, 40),
    'cur_grind_value_1': pygame.Rect(480, 60, 100, 40),
    'cur_grind_value_2': pygame.Rect(480, 120, 100, 40),
    'cur_grind_value_3': pygame.Rect(480, 180, 100, 40),
    'cur_grind_value_4': pygame.Rect(480, 240, 100, 40),
    'cur_gem_value_1': pygame.Rect(600, 60, 100, 40),
    'cur_gem_value_2': pygame.Rect(600, 120, 100, 40),
    'cur_gem_value_3': pygame.Rect(600, 180, 100, 40),
    'cur_gem_value_4': pygame.Rect(600, 240, 100, 40),
    'w_grind_value_1': pygame.Rect(740, 60, 100, 40),
    'w_grind_value_2': pygame.Rect(740, 120, 100, 40),
    'w_grind_value_3': pygame.Rect(740, 180, 100, 40),
    'w_grind_value_4': pygame.Rect(740, 240, 100, 40),
    'w_gem_value_1': pygame.Rect(860, 60, 100, 40),
    'w_gem_value_2': pygame.Rect(860, 120, 100, 40),
    'w_gem_value_3': pygame.Rect(860, 180, 100, 40),
    'w_gem_value_4': pygame.Rect(860, 240, 100, 40),
    'cur_sub_eff_value_1': pygame.Rect(1000, 60, 100, 40),
    'cur_sub_eff_value_2': pygame.Rect(1000, 120, 100, 40),
    'cur_sub_eff_value_3': pygame.Rect(1000, 180, 100, 40),
    'cur_sub_eff_value_4': pygame.Rect(1000, 240, 100, 40),
    'w_sub_eff_value_after_gg_1': pygame.Rect(1120, 60, 100, 40),
    'w_sub_eff_value_after_gg_2': pygame.Rect(1120, 120, 100, 40),
    'w_sub_eff_value_after_gg_3': pygame.Rect(1120, 180, 100, 40),
    'w_sub_eff_value_after_gg_4': pygame.Rect(1120, 240, 100, 40),
    'sp_eff_value_1': pygame.Rect(1240, 60, 100, 40),
    'sp_eff_value_2': pygame.Rect(1240, 120, 100, 40),
    'sp_eff_value_3': pygame.Rect(1240, 180, 100, 40),
    'sp_eff_value_4': pygame.Rect(1240, 240, 100, 40),
    'substat_1': pygame.Rect(20, 60, 200, 40),
    'substat_2': pygame.Rect(20, 120, 200, 40),
    'substat_3': pygame.Rect(20, 180, 200, 40),
    'substat_4': pygame.Rect(20, 240, 200, 40),
}