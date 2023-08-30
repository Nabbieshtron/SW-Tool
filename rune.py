import pygame
import re

from constants import (
    DEFAULT_RUNE_QUALITY,
    DISPLAY_RUNE,
    IN_APP_FONT,
    IN_APP_GRID,
    IN_APP_TEXT_COLOR,
    RUNE_QUALITY_BG_COLORS,
    RUNE_SETS,
)
from efficiency import Efficiency as Ef


class Rune:
    def __init__(self):
        self.efficiency = Ef()
        self.font = IN_APP_FONT
        
        # Rune data
        self.rune_data = {}
        
        # Rendered text
        self.render_data = {}

        # Rect
        self.rect_data = {}

    def render(self):
        # Aligning text to the left
        self.font.align = pygame.FONT_LEFT

        # Rune title
        self.render_data['title'] = self.font.render(self.rune_data['title'][0], True, IN_APP_TEXT_COLOR)
        
        # Rune main value
        text = ''
        if all(self.rune_data['main_value']):
            name, value, state = self.rune_data['main_value']
            text = f'{name} +{value}%' if state == 'no_flat' else f'{name} +{value}'
        self.render_data['main_value'] = self.font.render(text, True, IN_APP_TEXT_COLOR) 
        
        # Rune level, slot
        for key in ("level", "slot"):
            self.render_data[key] = self.font.render(self.rune_data[key][0]  , True, IN_APP_TEXT_COLOR)
        
        # Rune substats
        sub_text = ''
        grind_text = ''
        for sub_name, sub_value, grind, state in self.rune_data["sub_values"]:
            sub_text += f'{sub_name} +{sub_value}%\n' if state == 'no_flat' else f'{sub_name} +{sub_value}\n'
            grind_text += f'{grind}%\n' if state == 'no_flat' else f'{grind}\n'
            
        self.render_data["sub_values"] = self.font.render(sub_text,True,IN_APP_TEXT_COLOR)
        self.render_data["grinds"] = self.font.render(grind_text,True,IN_APP_TEXT_COLOR)
        
        # Roll efficiency
        self.render_data["roll_eff"] = self.font.render(
            "\n".join(str(round(value)) + "%" for value in self.efficiency.rune_roll_efficiency),
            True,
            IN_APP_TEXT_COLOR,
        )

        # Rune efficiency
        text = ''
        if self.rune_data["level"][0].isdigit() and len(self.rune_data["level"]) == 1 and 12 <= int(self.rune_data["level"][0]) <= 15:
            text = self.efficiency.rune_eff

        self.render_data["rune_eff"] = self.font.render(text, True, IN_APP_TEXT_COLOR)
        
    def creating_rect(self):
        # Level, slot
        for key in ("level", "slot"):
            self.rect_data[key] = self.render_data[key].get_rect(
                center=IN_APP_GRID[key].center
            )

        # Title, main value
        y = 20
        for key in ("title", "main_value"):
            self.rect_data[key] = self.render_data[key].get_rect(midtop=(300, y))
            y += 40

        # Rune substats
        self.rect_data["sub_values"] = self.render_data["sub_values"].get_rect(topleft=(100, 170))

        # Rune grinds
        self.rect_data["grinds"] = self.render_data["grinds"].get_rect(
            midtop=(IN_APP_GRID["grinds"].centerx, self.rect_data["sub_values"].top)
        )

        # Roll efficiency
        self.rect_data["roll_eff"] = self.render_data["roll_eff"].get_rect(
            midtop=(IN_APP_GRID["roll_eff"].centerx, self.rect_data["sub_values"].top)
        )

        # Rune efficiency
        self.rect_data["rune_eff"] = self.render_data["rune_eff"].get_rect(
            center=IN_APP_GRID["rune_eff"].center)

    def preparing_data(self, data):
        def split_parts(text):
            return re.findall('[A-Za-z ]+|[^A-Za-z €()]+', text)
            
        def parse_record(s):
            return [list(t) for t in rx.findall(s)]
            
        def add_spaces(text):
            text = re.sub('([a-z])([A-Z])', r'\g<1> \g<2>', text)
            text = re.sub('([A-Z])([A-Z])([a-z])', r'\g<1> \g<2>\g<3>', text)
            return text
        
        # Detecting if substat value is flat (flat = value without percent)
        def check_flat(value:str):
            return "no_flat" if "%" in value else "flat"
            
        # Removing noise from values
        def remove_noise(value:str):
            values = re.findall('[0-9]+', value)
            return values[0] if values else '0'
            
        
        # Adding correct spacing between values
        output = {}
        for key,value in data.items():
            value = value.replace('\n','').replace(' ', '')
            if type(value) is str:
                output[key] = add_spaces(value)
            if key != 'sub_values':
                output[key] = split_parts(add_spaces(output[key]))
        
        data = output
        print(data)
        # Setting slot and level value
        if len(data['title']) == 3 and '+' in data['title'][0] and 'Rune' in data['title'][1]:
            data['slot'] = [data['title'].pop(-1)]
            data['level'] = [data['title'].pop(0).strip('+')]
        else:
            data['level'] = ['']
            data['slot'] = ['']
            data['title'] = ['Adjust the image']
            
        # Preparing main values of the rune
        if len(data['main_value']) == 2:
            main_value = data['main_value'][1]
            
            # Checking state
            state = check_flat(main_value)
            
            # Removing noise
            data['main_value'][1] = remove_noise(main_value)
            
            # Appending state
            data['main_value'].append(state)
        else:
            data['main_value'] = ['','','']

        # Preparing sub_status of the rune
        rx = re.compile(r'([a-ik-zA-IK-Z]+(?:\s+[a-zA-Z]+)?)\s*(\+\d+%?)\s*(\+\d+%?)?')
        data['sub_values'] = parse_record(data['sub_values'])
        
        output = []
        for sub_name, sub_value, grind in data['sub_values']:
            # Checking state
            state = check_flat(sub_value)
            
            # Removing noise
            value = remove_noise(sub_value)
            grind = remove_noise(grind)
            
            output.append([sub_name, value, grind, state])
            
        data['sub_values'] = output
        
        # Preparing the rune default grade
        if data['default_grade']:
            grade = data['default_grade'][0].strip('\n')
            if grade[0] == 'A':
                grade = grade.replace('A', 'Ancient')
            data['default_grade'] = [grade]
        else:
            data['default_grade'] = []
            
        self.rune_data = data

        
    def update(self, data):
        if data:
            # Preparing data for use
            self.preparing_data(data)
            
            # Calculating rune efficiency
            self.efficiency.update(self.rune_data)
            
            # Rendering text
            self.render()
            
            # Creatinging Rect()
            self.creating_rect()
            
    def draw(self, surface):
        for key in self.render_data:
            surface.blit(self.render_data[key], self.rect_data[key])

        # Border Lines
        pygame.draw.rect(surface, "White", pygame.Rect((0, 0), DISPLAY_RUNE), 2, 1)
        
        # Side grid
        for key in IN_APP_GRID:
            pygame.draw.rect(surface, "White", IN_APP_GRID[key], 2, 1)
        
        
        for key, value in self.efficiency.grades.items():
            if 'ancient' in value:
                value = 'legend'
            if value:
                pygame.draw.rect(
                    surface,
                    RUNE_QUALITY_BG_COLORS[value],
                    IN_APP_GRID[key],
                )
                surface.blit(
                    DEFAULT_RUNE_QUALITY[value],
                    DEFAULT_RUNE_QUALITY[value].get_rect(
                        center=IN_APP_GRID[key].center
                    ),
                )
                
            # Top grid
            pygame.draw.rect(surface, "White", IN_APP_GRID[key], 2)

        pygame.draw.rect(surface, "White", IN_APP_GRID["grinds"], 2, 1)
        pygame.draw.rect(surface, "White", IN_APP_GRID["roll_eff"], 2, 1)
