import pygame
import copy
from dataclasses import dataclass, fields
from functools import partial

from widgets import ListBox, TextBox
from constants import (
    MAIN_POWER_UP,
    DEFAULT_CONFIGURATIONS,
    GRIND_MANAGER_FONT,
    GRIND_MANAGER_RECTS,
    RUNE_SETS,
    SUB_VALUES,
    START_BG_COLOR,
)


class RuneBox:
    def __init__(self, id_:str, rune: 'Rune', rects:dict[str:pygame.Rect]):
        self.id_ = id_
        self.rune = rune
        self.rects = rects
        self.draw_menu = False
        self.menu_active = False
        self.rendered = self.render_text()
        self.list_boxes = self.generate_list_boxes()
        self.text_boxes = self.generate_text_boxes()
    
    def generate_list_boxes(self) -> dict:
        list_boxes = {}
        list_boxes['level'] = ListBox(
            color_menu=['Pink', 'Light pink'],
            color_option=['Blue', 'Light blue'],
            rect=self.rects['level'],
            font=GRIND_MANAGER_FONT,
            main=str(self.rune.level),
            options=[str(n) for n in range(1,16)],
            amount_showed=5,
        )
        list_boxes['slot'] = ListBox(
            color_menu=['Pink', 'Light pink'],
            color_option=['Blue', 'Light blue'],
            rect=self.rects['slot'],
            font=GRIND_MANAGER_FONT,
            main=self.rune.slot,
            options=[str(n) for n in range(1,7)],
            amount_showed=5,
        )
        list_boxes['set'] = ListBox(
            color_menu=['Pink', 'Light pink'],
            color_option=['Blue', 'Light blue'],
            rect=self.rects['set'],
            font=GRIND_MANAGER_FONT,
            main=self.rune.set_,
            options=[set_.upper() for set_ in RUNE_SETS],
            amount_showed=5,
        )
        list_boxes['main'] = ListBox(
            color_menu=['Pink', 'Light pink'],
            color_option=['Blue', 'Light blue'],
            rect=self.rects['main'],
            font=GRIND_MANAGER_FONT,
            main=self.rune.main.name,
            options=[sub.upper() for sub in SUB_VALUES],
            amount_showed=5,
        )
        list_boxes['innate'] = ListBox(
            color_menu=['Pink', 'Light pink'],
            color_option=['Blue', 'Light blue'],
            rect=self.rects['innate'],
            font=GRIND_MANAGER_FONT,
            main=self.rune.innate.name,
            options=[sub.upper() for sub in SUB_VALUES],
            amount_showed=5,
        )
        for n, substat in enumerate(self.rune.substats, 1):
            list_boxes[f'substat_{n}'] = ListBox(
                color_menu=['Pink', 'Light pink'],
                color_option=['Blue', 'Light blue'],
                rect=self.rects[f'substat_{n}'],
                font=GRIND_MANAGER_FONT,
                main=substat.name,
                options=[sub.upper() for sub in SUB_VALUES],
                amount_showed=5,
            )
        return list_boxes
        
    def generate_text_boxes(self) -> dict['str', 'TextBox']:
        text_boxes = {}
        text_boxes['cur_grind_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_grind_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_grind_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_grind_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_grind_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_grind_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_grind_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_grind_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_gem_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_gem_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_gem_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_gem_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_gem_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_gem_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_gem_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_gem_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_grind_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_grind_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_grind_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_grind_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_grind_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_grind_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_grind_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_grind_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_gem_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_gem_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_gem_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_gem_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_gem_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_gem_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_gem_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_gem_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_eff_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_eff_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_eff_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_eff_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_eff_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_eff_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_eff_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_eff_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_sub_eff_value_after_gg_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_sub_eff_value_after_gg_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_sub_eff_value_after_gg_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_sub_eff_value_after_gg_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_sub_eff_value_after_gg_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_sub_eff_value_after_gg_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['w_sub_eff_value_after_gg_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['w_sub_eff_value_after_gg_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['sp_eff_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['sp_eff_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['sp_eff_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['sp_eff_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['sp_eff_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['sp_eff_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['sp_eff_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['sp_eff_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['main_value'] = TextBox(
            main='1500',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['main_value'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['innate_value'] = TextBox(
            main='8',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['innate_value'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['def_sub_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['def_sub_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['def_sub_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['def_sub_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['def_sub_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['def_sub_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['def_sub_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['def_sub_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_value_1'] = TextBox(
            main='1559',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_value_1'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_value_2'] = TextBox(
            main='10',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_value_2'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_value_3'] = TextBox(
            main='11',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_value_3'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['cur_sub_value_4'] = TextBox(
            main='12',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['cur_sub_value_4'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
            char_type='DIGIT',
            char_limit=4,
        )
        text_boxes['r_efficiency'] = TextBox(
            main='r.eff',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['r_efficiency'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
        )
        text_boxes['rp_efficiency'] = TextBox(
            main='rp.eff',
            font=GRIND_MANAGER_FONT,
            rect=self.rects['rp_efficiency'],
            color_active=['Black', 'White'],
            color_menu=['Pink', 'Light pink'],
        )
        return text_boxes
        
    @classmethod
    def from_dict(cls, data: dict[str,dict]) -> dict[str, "RuneBox"]:
        boxes = {}
        for i, (id_, rune) in enumerate(data.items()):
            rects = {k: v.move(0, i*50) for k, v in GRIND_MANAGER_RECTS.items()}
            boxes[id_] = cls(id_, rune, rects)
        return boxes
        
    def render_text(self):
        surf = GRIND_MANAGER_FONT.render(self.id_.replace('ID_', ''), True, 'Black')
        rect = surf.get_rect(center=self.rects['id'].center)
        return (surf, rect)
        
    def dispatch_events(self, e):
        for key, box in self.text_boxes.items():
            box.dispatch_events(e)
        
        for key, box in reversed(self.list_boxes.items()):
            box.dispatch_events(e)
            
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.menu_active:
            self.draw_menu = not self.draw_menu
        
    def update(self):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rects['id'].collidepoint(mpos)
        for key, box in self.text_boxes.items():
            box.update()
        
        for key, box in reversed(self.list_boxes.items()):
            print(key,'\n', box.rect)
            box.update()
        
    def draw(self, screen):
        screen.fill(START_BG_COLOR)

        # Grid
        for key, rect in self.rects.items():
            if self.draw_menu or key in (
                'id',
                'level',
                'slot',
                'set',
                'main',
                'innate',
                'main_value',
                'innate_value',
                'r_efficiency',
                'rp_efficiency',
            ):
                pygame.draw.rect(screen, 'Pink', rect)
                pygame.draw.rect(screen, 'Black', rect, 2, 1)
        
        # Text
        screen.blit(*self.rendered)
            
        # Text boxes
        for key, box in self.text_boxes.items():
            if self.draw_menu or key in (
                'id',
                'level',
                'slot',
                'set',
                'main',
                'innate',
                'main_value',
                'innate_value',
                'r_efficiency',
                'rp_efficiency',
            ):
                box.draw(screen)
            
        # List boxes
        for key, box in reversed(self.list_boxes.items()):
            if self.draw_menu or key in (
                'id',
                'level',
                'slot',
                'set',
                'main',
                'innate',
                'main_value',
                'innate_value',
                'r_efficiency',
                'rp_efficiency',
            ):
                box.draw(screen)


@dataclass
class RuneData:
    name: str
    value: int
    grind: str = ''
    gem: str = ''
    flat: bool = False

    @classmethod
    def from_tuple(cls, data: tuple[str, int, str, str, bool]) -> "RuneData":
        obj = cls(*data)
        name = obj.name.lower()
        if name in SUB_VALUES:
            obj.flat = SUB_VALUES[name][-1]
        return obj


@dataclass
class Rune:
    title: str
    grade: str
    main: RuneData
    set_: str
    slot: str
    level: int
    innate: RuneData
    substats: list[RuneData]
    default_sub_value: bool = False # Load from saves, false init
    substat_modifiers = DEFAULT_CONFIGURATIONS.get('efficiency_multipliers') # Load from saves, false init, figure out if have default value in code or not
    
    def __post_init__(self):
        self.substats_efficiency = self.get_value_efficiency(self.substats)
        self.innate_efficiency = self.get_value_efficiency((self.innate,))
        self.efficiency = self.get_efficiency()
        self.substats_grade = self.get_substats_grade()
    
    @classmethod
    def from_dict(cls, data: dict) -> "Rune":
        params = {}
        for field in fields(cls):
            if (value := data.get(field.name)) is not None:
                if field.type is RuneData:
                    value = RuneData.from_tuple(tuple(value))
                elif field.type == list[RuneData]:
                    value = [RuneData.from_tuple(tuple(i)) for i in value]
                    for obj in value:
                        name = obj.name.lower()
                        if name in SUB_VALUES:
                            obj.flat = SUB_VALUES[name][-1]
                params[field.name] = value
        return cls(**params)
        
    def get_value_efficiency(self, object_tpl:tuple[RuneData]) -> list:
        '''Method to calculate substats efficiency values'''
        efficiency = []

        for obj in object_tpl:
            name = obj.name.lower()
            if name in SUB_VALUES:
                if obj.flat and 'flat' not in name and name != 'spd':
                    name += ' flat'
                highest_value = SUB_VALUES[name][1]  
                value = (obj.value / highest_value) * 100

                # Removing the defualt sub value -> user modifiable
                if self.default_sub_value is False:
                    value -= 100

                # parse value
                value = 0 if value < 0 else round(value)

                efficiency.append(value)
                
        return list(efficiency)
        
    def get_substats_grade(self): 
        if len(self.substats_efficiency) == 4:
            total = sum(self.substats_efficiency)
            if total > 300:
                return "legend"
            elif total > 200:
                return "hero"
            elif total > 100:
                return "rare"
            elif total > 0:
                return "magic"
        return 'NONE' 

    def get_efficiency(self) -> int:
        ratio:float = 0
        percent:int = lambda part, whole: int(whole / 100 * part + whole)
        
        # Main
        name = self.main.name.lower()
        if self.level and 12 <= self.level <= 15 and name in MAIN_POWER_UP:
            power_up = [obj for obj in MAIN_POWER_UP.get(name) if obj.flat is self.main.flat]

            for obj in power_up:
                # Calculating max value
                if self.level == 15:
                    max_value = percent(20, (self.level-1) * obj.increment + obj.start)
                else:
                    max_value = self.level * obj.increment + obj.start

                # Calculating ratio
                if max_value == self.main.value:
                    if obj.grade == 6:
                        ratio = 1.0
                    elif obj.grade == 5:
                        end_values = [obj.end for obj in power_up]
                        ratio = min(end_values) / max(end_values)

        else:
            ratio = 0

        # Sub stat, Add innate?
        if ratio > 0:
            for substat in self.substats:
                name = substat.name.lower()
                if substat.flat and name != 'spd':
                    name += ' flat'
                    
                if name in SUB_VALUES:
                    highest_value = SUB_VALUES[name][1]
                    substat_modifier = self.substat_modifiers[name]
 
                    ratio += (
                        substat.value
                        / highest_value
                        * 0.2
                        * float(substat_modifier)
                    )
                else:
                    ratio = 0
                    break

        # Calculate efficiency
        return round((ratio / 2.8) * 100) if ratio > 0 else ''