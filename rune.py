import pygame
import cv2
import re
import json
import pathlib

from constants import (
    DEFAULT_SUB_VALUES,
    DEFAULT_MAIN_POWER_UP,
    RUNE_QUALITY,
    RUNE_QUALITY_BG_COLORS,
    IN_APP_FONT,
    IN_APP_GRID,
    IN_APP_TEXT_COLOR,
    IN_APP_BG_COLOR,
    DISPLAY_SIZES,
    BUTTON_TEXTS,
    BUTTON_RECTS,
    ELEVATION,
    BUTTON_FONT,
    BUTTON_TEXT_COLOR,
    BUTTON_BG_COLORS,
    BUTTON_HOVER_COLOR,
    RUNE_SETS,
    DEFAULT_PREFERENCES
)
from button import Button
from game_state import GameState
from tesseract import Tesseract
from PIL import ImageGrab as PilIg
import numpy as np

class Rune(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.persist = persist
        self.tesseract = Tesseract()
        self.images = {}
        self.font = IN_APP_FONT
        
        # Path
        self.save_path = save_path
            
        # Rune info
        self.title = ''
        self.main = ['', 0]
        self.rune_set = ''
        self.innate = ''
        self.substats = []
        self.substats_grade = ''
        self.grade = ''
        self.level = ''
        self.slot = ''
        self.roll_efficiency = []
        self.efficiency = ''
        
        # Button that save the rune information
        self.button_save = Button(
            BUTTON_RECTS['save'],
            ELEVATION,
            BUTTON_TEXTS['save'],
            BUTTON_FONT,
            BUTTON_TEXT_COLOR,
            BUTTON_BG_COLORS,
            BUTTON_HOVER_COLOR,
            self.add_rune
            )
        
        # Include default value in the efficiency calculations (User replacabale)
        self.default_value = DEFAULT_PREFERENCES['efficiency_default_value']
        
        # Default value of efficiency multiplier (User replacabale)
        self.substat_modifiers = DEFAULT_PREFERENCES['efficiency_multipliers']
        
        self.rendered_objs = []
        
    def preparing_data(self, data):
        output = {}
        # Adding correct spacing between values
        for key in ('title','main','innate','substats','grade'):
            if type(data[key]) is str:
                value = data[key].replace('\n','').replace(' ', '')
                value = re.sub('([a-z])([A-Z])', r'\g<1> \g<2>', value)
                output[key] = re.sub('([A-Z])([A-Z])([a-z])', r'\g<1> \g<2>\g<3>', value)
            if key not in ('substats', 'grade'):
                output[key] = re.findall('[A-Za-z ]+|[^A-Za-z €()]+', output[key])

        # Slot, level, title, rune_set
        if len(output['title']) == 3 and '+' in output['title'][0] and 'rune' in output['title'][1].lower():
            level, title, slot = output['title']
            output['slot'] = re.findall('[1-6]', slot)[0]
            output['level'] = re.findall('[0-9]+', level)[0]
            output['title'] = title
            for text in title.split():
                text = text.lower().strip()
                if text in RUNE_SETS:
                    i = RUNE_SETS.index(text)
                    output['rune_set'] = RUNE_SETS[i]
        else:
            output['level'] = ''
            output['slot'] = ''
            output['rune_set'] = ''
            output['title'] = 'Adjust the image'
        
        # Main
        if len(output['main']) == 2:
            name, value = output['main']
            
            # Changing name depending if its flat or not
            if "%" not in value:
                name = f"flat_{name}"
                
            # Removing noise
            no_noise = re.findall('[0-9]+', value)
            value = no_noise[0] if no_noise else '0'
            output['main'] =  [name, value]
        else:
            output['main'] = ['',0]

        # Substats
        rx = re.compile(r'([a-ik-zA-IK-Z]+(?:\s+[a-zA-Z]+)?)\s*(\+\d+%?)\s*(\+\d+%?)?')
        substats = [list(t) for t in rx.findall(output['substats'])]
        output['substats'] = []
        
        for sub_name, sub_value, grind in substats:
            if "%" not in sub_value:  
                sub_name = f"flat_{sub_name}"
            
            # Removing noise
            no_noise_sub_value = re.findall('[0-9]+', sub_value)
            no_noise_grind = re.findall('[0-9]+', grind)
            sub_value = no_noise_sub_value[0] if no_noise_sub_value else '0'
            grind = no_noise_grind[0] if no_noise_grind else '0'
            
            output['substats'].append([sub_name, sub_value, grind])
        
        # Updating attributes
        vars(self).update(output)

    def processing_image(self, image):
        window_rect = self.persist['window_dim_attribute']
        transparent_rect = self.persist['transparent_dim']
        navigation_rects = self.persist['navigation_dims_attributes']

        for key, _rect in navigation_rects.items():
            # Calculating the new _rect position
            # Note !!! w and h need self.screen for more accurate calculations
            x = window_rect.x + _rect.x
            y = window_rect.y + _rect.y
            w = window_rect.w - transparent_rect.y - (transparent_rect.right - _rect.right)
            h = window_rect.h - transparent_rect.y - (transparent_rect.bottom - _rect.bottom)

            # Croping the image from main image
            cropped_img = image[y:h, x:w]
            
            # Invert image
            inverted_image = cv2.bitwise_not(cropped_img)

            # Gray scaled image
            gray_scaled_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)

            # Binaryse the image (make it black and white)
            threshold_value = 170
            max_value = 230
            if key == 'grade':
                threshold_value = 130
                max_value = 230
                
            thresh, image_bw = cv2.threshold(gray_scaled_image, threshold_value, 
                max_value, cv2.THRESH_BINARY)

            self.images[key] = image_bw
    
    # Checking sub-status roll efficiency
    def get_roll_efficiency(self):
        self.roll_efficiency = []
        for sub_name, sub_value, _ in self.substats:
            if sub_name.lower() in DEFAULT_SUB_VALUES:
                # Calculating roll efficiency value
                value = (
                    int(sub_value) / DEFAULT_SUB_VALUES[sub_name.lower()][1]
                ) * 100

                # Removing the defualt value
                if self.default_value is False:
                    value -= 100

                # if negative value = 0, else rounding the value
                value = 0 if value < 0 else round(value)

                self.roll_efficiency.append(value)

    # Calculating efficiency
    def get_efficiency(self):
        ratio:float = 0.0
        percent:int = lambda part, whole: int(whole / 100 * part + whole)
        name, value = self.main
        level = int(self.level) if self.level else 0

        # Adding main value ratio
        if all(self.main) and 12 <= level <= 15 and name.lower() in DEFAULT_MAIN_POWER_UP:
            basic, increment, highest = DEFAULT_MAIN_POWER_UP[name.lower()]
            # Calculating maxed rune main value
            if level == 15:
                level -= 1
                six_star = percent(20, level * increment[1] + basic[1])
                five_star = percent(20, level * increment[0] + basic[0])
            else:
                six_star = level * increment[1] + basic[1]
                five_star = level * increment[0] + basic[0]

            # Checking rune "star" grade
            if six_star == int(value):
                ratio += 1.0
            elif five_star == int(value):
                ratio += highest[0] / highest[1]
            else:
                print("Efficiency Error")
        else:
            ratio = 0
        
        # Sub stat , inates
        if ratio > 0:
            for sub_name, sub_value, _ in self.substats:
                sub_name, sub_value = sub_name.lower(), int(sub_value)
                if sub_name in DEFAULT_SUB_VALUES:
                    ratio += (
                        sub_value
                        / DEFAULT_SUB_VALUES[sub_name][1]
                        * 0.2
                        * float(self.substat_modifiers[sub_name])
                    )
                else:
                    ratio = 0
                    break

        # Calculate efficiency
        self.efficiency = str(round((ratio / 2.8) * 100)) if ratio > 0 else ''
        
    def get_substats_grade(self): 
        # Only if max amount of substatus values
        if len(self.roll_efficiency) == 4:
            total = sum(self.roll_efficiency)
            if total > 300:
                self.substats_grade =  "legend"
            elif total > 200:
                self.substats_grade =  "hero"
            elif total > 100:
                self.substats_grade =  "rare"
            elif total > 0:
                self.substats_grade =  "magic"
            else:
                self.substats_grade = ""
        else:
            self.substats_grade = ""
    
    def add_rune(self):
        attributes = ['title', 'rune_set', 'slot', 'level', 'grade', 'substats']
        id_nr = 1
        limit = 2000
        if all([getattr(self, name, False) for name in attributes]):
            while limit:
                rune_id = f"ID_R{str(id_nr)}"
                if rune_id not in self.persist['runes'][rune_id]:
                    self.persist['runes'][rune_id] = {
                        'title': self.title,
                        'set': self.rune_set,
                        'slot': self.slot,
                        'level': self.level,
                        'grade': self.grade,
                        'innate': self.innate,
                        'substats': self.substats
                    }
                    break
                else:
                    limit -= 1
                    id_nr+=1
                    continue

    def save(self):
        if self.persist['runes']:
            with open(self.save_path, "w") as file:
                try:
                    json.dump(self.persist['runes'], file, indent=4)
                except json.JSONDecodeError:
                    print("Saving rune error")

    def rendering(self):
        self.rendered_objs = []
        
        # Aligning text to the left
        self.font.align = pygame.FONT_LEFT

        # Title
        title = self.font.render(self.title, True, IN_APP_TEXT_COLOR)
        title_rect = title.get_rect(midtop=(300, 20))
        self.rendered_objs.append([title, title_rect])

        # Main
        main = ''
        end_with = ''
        if all(self.main):
            name, value = self.main
            end_with = '%' if 'flat' not in name else ''
            name = name.replace('flat_', '')
            main = f'{name} +{value}{end_with}'
            
        main = self.font.render(main, True, IN_APP_TEXT_COLOR) 
        main_rect = main.get_rect(midtop=(300, 60))
        self.rendered_objs.append([main, main_rect])
        
        # Level, Slot
        for key in ('level', 'slot'):
            obj = self.font.render(vars(self)[key], True, IN_APP_TEXT_COLOR)
            obj_rect = obj.get_rect(center=IN_APP_GRID[key].center)
            self.rendered_objs.append([obj, obj_rect])

        # Substats, grinds
        substats = ''
        grinds = ''
        for sub_name, sub_value, grind in self.substats:
            end_with = '%' if 'flat' not in sub_name else ''
            sub_name = sub_name.replace('flat_', '')
            substats += f'{sub_name} +{sub_value}{end_with}\n'
            grinds += f'{grind}{end_with}\n'

        substats = self.font.render(substats,True,IN_APP_TEXT_COLOR)
        substats_rect = substats.get_rect(topleft=(100, 170))
        self.rendered_objs.append([substats, substats_rect])
        
        grinds = self.font.render(grinds,True,IN_APP_TEXT_COLOR)
        grinds_rect = grinds.get_rect(midtop=(IN_APP_GRID["grinds"].centerx, substats_rect.top))
        self.rendered_objs.append([grinds, grinds_rect])
        
        # Roll efficiency
        roll_efficiency = "\n".join([str(value)+'%' for value in self.roll_efficiency])
        roll_efficiency = self.font.render(roll_efficiency,True,IN_APP_TEXT_COLOR,)
        roll_efficiency_rect = roll_efficiency.get_rect(
            midtop=(IN_APP_GRID["roll_efficiency"].centerx, substats_rect.top))
        self.rendered_objs.append([roll_efficiency, roll_efficiency_rect])
        
        # Rune efficiency 
        efficiency = self.font.render(self.efficiency, True, IN_APP_TEXT_COLOR)
        efficiency_rect = efficiency.get_rect(center=IN_APP_GRID["rune_efficiency"].center)
        self.rendered_objs.append([efficiency, efficiency_rect])

    def dispatch_event(self, e):
        self.button_save.dispatch_event(e)
        
        if e.type == pygame.QUIT:
            self.running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.save()
            self.app.next_state('main_menu', self.persist)
            self.app.set_window('main_menu', True)

    def update(self, dt):
        screenshot = PilIg.grab(all_screens=False)
        
        # Convert pil to cv2
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        if self.tesseract.data_thread is None and self.tesseract.text_thread is None:
            self.processing_image(image)

        # Getting and preparing text
        self.tesseract.update(self.images)
        self.preparing_data(self.tesseract.text)

        # Efficiency
        self.get_roll_efficiency()
        self.get_efficiency()
        self.get_substats_grade()

        self.button_save.update()
        self.rendering()

    def draw(self, screen):
        # Bg color
        screen.fill(IN_APP_BG_COLOR)
        
        self.button_save.draw(screen)
        
        for obj, pos in self.rendered_objs:
            screen.blit(obj, pos)
        
        if self.grade and self.substats_grade:
            for key in ('grade', 'substats_grade'):
                attrs = vars(self)
                pygame.draw.rect(
                    screen,
                    RUNE_QUALITY_BG_COLORS[attrs[key].lower()],
                    IN_APP_GRID[key]
                    )

                screen.blit(
                    RUNE_QUALITY[attrs[key].lower()],
                    RUNE_QUALITY[attrs[key].lower()].get_rect(center=IN_APP_GRID[key].center)
                    )
        
        # Border Lines
        pygame.draw.rect(screen, "White", pygame.Rect((0, 0), DISPLAY_SIZES['start']), 2, 1)

        # Side grid
        for key in IN_APP_GRID:
            pygame.draw.rect(screen, "White", IN_APP_GRID[key], 2, 1)