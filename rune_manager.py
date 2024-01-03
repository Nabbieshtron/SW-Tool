import pygame
import cv2
import json
import pathlib
import numpy as np

from PIL import ImageGrab as PilIg
from functools import partial

from user_config import save_runes
from button import Button
from game_state import GameState
from tesseract import Tesseract
from rune import Rune
from widgets import ListBox, TextBox
from constants import (
    DISPLAY_SIZES,
    RUNE_SETS,
    RUNE_SLOTS,
    RUNE_LEVEL,
    SUB_VALUES,
    START_FONT,
    START_BG_COLOR,
    START_TEXT_COLOR,
    START_GRID,
    RUNE_GRADES,
    TEXT_BOX_COLOR,
)

class RuneManager(GameState):
    def __init__ (self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.persist = persist
        self.tesseract = Tesseract()
        self.tese_images = {}
        self.imgs = {}
        self.font = START_FONT
        self.text_color = START_TEXT_COLOR
        self.rendered_objs = []
        self.rune_obj = None
        
        # Path
        self.save_path = save_path
        
        self.buttons = {}
        self.buttons['save'] = Button(
            text='Save',
            font=pygame.font.SysFont("Arial", 30),
            rect=pygame.Rect((620,550,150,35)),
            method=self.saving,
            elevation=6,
            top_color="#475F77",
            bottom_color="#354B5E",
            text_color="#FFFFFF",
            collide_color="#D74B4B",
        )
        
        self.text_boxes = {}
        for n in range(1,7):
            key = f'value_{n}'
            self.text_boxes[key] = TextBox(
                main='',
                font=pygame.font.SysFont('Arial', 26),
                rect=pygame.Rect(840, 112+(60*(n-1)), 100, 40),
                color_active=TEXT_BOX_COLOR,
                color_menu=['Pink', 'Light pink'],
                char_type='DIGIT',
                char_limit=4,
            )
            
            if n > 4:
                continue
                
            key = f'grind_{n}'
            self.text_boxes[key] = TextBox(
                main='',
                font=pygame.font.SysFont('Arial', 26),
                rect=pygame.Rect(960, 232+(60*(n-1)), 100, 40),
                color_active=TEXT_BOX_COLOR,
                color_menu=['Pink', 'Light pink'],
                char_type='DIGIT',
                char_limit=4,
            )
            key = f'gem_{n}'
            self.text_boxes[key] = TextBox(
                main='',
                font=pygame.font.SysFont('Arial', 26),
                rect=pygame.Rect(1080, 232+(60*(n-1)), 100, 40),
                color_active=TEXT_BOX_COLOR,
                color_menu=['Pink', 'Light pink'],
                char_type='DIGIT',
                char_limit=4,
            )
        
        self.list_boxes = {}
        
        self.list_boxes['slot'] = ListBox(
            color_menu=['Dark Red','Red'],
            color_option=['Dark Orange','Orange'],
            rect=pygame.Rect(840, 30, 100, 40),
            font=pygame.font.SysFont('Arial', 26),
            main='',
            options=RUNE_SLOTS,
            amount_showed=4
        )
        self.list_boxes['set_'] = ListBox(
            color_menu=['Dark Red','Red'],
            color_option=['Dark Orange','Orange'],
            rect=pygame.Rect(960, 30, 220, 40),
            font=pygame.font.SysFont('Arial', 26),
            main='',
            options=[rset.upper() for rset in RUNE_SETS],
            amount_showed=4
        )
        self.list_boxes['level'] = ListBox(
            color_menu=['Dark Red','Red'],
            color_option=['Dark Orange','Orange'],
            rect=pygame.Rect(720, 30, 100, 40),
            font=pygame.font.SysFont('Arial', 26),
            main='',
            options=RUNE_LEVEL,
            amount_showed=4
        )
        
        for n, key in enumerate(
            ('main', 'innate', 'substat_1', 'substat_2', 'substat_3', 'substat_4')
        ):
            self.list_boxes[key] = ListBox(
                color_menu=['Dark Red','Red'],
                color_option=['Dark Orange','Orange'],
                rect=pygame.Rect(620, 112+n*60, 200, 40),
                font=pygame.font.SysFont('Arial', 26),
                main='',
                options=[key.upper() for key in SUB_VALUES],
                amount_showed=4,
            )

        # Limited count id generator
        rune_limit = 2000
        self.id_generator = (f"ID_R{str(n)}" for n in range(1, rune_limit))
    
    def load_images(self):
        self.imgs['violent'] = pygame.image.load('assets/images/rune/slot_1/violent.jpg').convert()   
    
    def saving(self):
        save_data = {}
        save_data['title'] = 'Not implemented'
        save_data['grade'] = 'Not implemented'
        
        level = getattr(self.list_boxes['level'], 'main', '')
        if level or level.isdigit():
            level = int(level)
        else:
            level = 0
        save_data['level'] = level
        
        save_data['slot'] = getattr(self.list_boxes['slot'], 'main', '')
        save_data['set_'] = getattr(self.list_boxes['set_'], 'main', '')
        
        value = getattr(self.text_boxes['value_1'], 'main', '')
        if value or value.isdigit():
            value = int(value)
        else:
            value = 0
        save_data['main'] = [
            getattr(self.list_boxes['main'], 'main', ''), 
            value
        ]
        
        value = getattr(self.text_boxes['value_2'], 'main', '')
        if value or value.isdigit():
            value = int(value)
        else:
            value = 0  
        save_data['innate'] = [
            getattr(self.list_boxes['innate'], 'main', ''),
            value,
        ]

        substats = []
        for n in range(1, 5):
            value = getattr(self.text_boxes[f'value_{2+n}'], 'main', '')
            if value or value.isdigit():
               value = int(value)
            else:
                value = 0
                
            substats.append([
                getattr(self.list_boxes[f'substat_{n}'], 'main', ''),
                value,
                getattr(self.text_boxes[f'grind_{n}'], 'main', ''),
                getattr(self.text_boxes[f'gem_{n}'], 'main', '')
            ])
            
        save_data['substats'] = substats
        
        if all([save_data[x] for x in save_data if x in('main','level','slot','set_','substats')]):
            for rune_id in self.id_generator:
                if rune_id not in self.persist['runes']:
                    save_runes({rune_id:save_data}, self.save_path)
                    self.persist['runes'] = {rune_id:Rune.from_dict(save_data)}
                    break
            else:
                print("Rune limit reached")
        else:
            print("Saving requirements not met")
        
    def processing_image(self, image):
        # Core rects for image cropping
        window_rect = pygame.Rect(*self.persist['window_rect_attribute'].values())
        transparent_rect = pygame.Rect(*self.persist['transparent_rect'].values())
        navigation_rects = {}
        for key, dims in self.persist['navigation_rect_attributes'].items():
            navigation_rects[key] = pygame.Rect(*dims.values())
            
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

            self.tese_images[key] = image_bw
    
    def update_boxes(self, obj:Rune):
        self.text_boxes['value_1'].main = str(getattr(obj.main, 'value', ''))
        self.text_boxes['value_2'].main = str(getattr(obj.innate, 'value', ''))

        for n, sub in enumerate(obj.substats, 1):
            self.list_boxes[f'substat_{n}'].main = getattr(sub, 'name', '').upper()
            self.text_boxes[f'value_{2+n}'].main = str(getattr(sub, 'value', ''))
            self.text_boxes[f'grind_{n}'].main = getattr(sub, 'grind', '')
            self.text_boxes[f'gem_{n}'].main = getattr(sub, 'gem', '')
            
        self.list_boxes['set_'].main = getattr(obj, 'set_', '').upper()
        self.list_boxes['level'].main = str(getattr(obj, 'level', ''))
        self.list_boxes['slot'].main = getattr(obj, 'slot', '')
        self.list_boxes['main'].main = getattr(obj.main, 'name', '').upper()
        self.list_boxes['innate'].main = getattr(obj.innate, 'name', '').upper()

        
    def render(self, rune: Rune):
        self.rendered_objs = []
        
        # Title, Main
        self.font.align = pygame.FONT_CENTER
        
        end_with = '\n' if rune.main.flat else '%\n'
        if rune.main.name:
            main = f'{rune.main.name} +{str(rune.main.value)}{end_with}'
            title = f'{rune.title}\n{main}'
        else:
            title = rune.title
            
        surface = self.font.render(title, True, self.text_color)
        surface_rect = surface.get_rect(midtop = (300, 15))
        self.rendered_objs.append([surface, surface_rect])
        
        # Level, Slot, Rune efficiency
        for key in ('level', 'slot', 'efficiency'):
            surface = self.font.render(str(rune.__dict__.get(key)), True, self.text_color)
            surface_rect = surface.get_rect(center=START_GRID[key].center)
            self.rendered_objs.append([surface, surface_rect])
        
        # Substat, Innate
        self.font.align = pygame.FONT_LEFT
        substats = ''   
        grinds = ''

        if rune.innate.name and rune.innate.value:
           end_with = '' if rune.innate.flat else '%'
           substats = f'{rune.innate.name} +{str(rune.innate.value)}{end_with}\n'

        for substat in rune.substats:
            end_with = '' if substat.flat else '%'
            substats += f'{substat.name} +{str(substat.value)}{end_with}\n'
            grinds += f'+{substat.grind}{end_with}\n' if substat.grind else '\n'

        surface = self.font.render(substats, True, self.text_color)
        surface_rect = surface.get_rect(topleft=(100, 170))
        self.rendered_objs.append([surface, surface_rect])

        if grinds.strip():
            surface = self.font.render(grinds, True, self.text_color)
            surface_rect = surface.get_rect(midtop=(START_GRID["grinds"].centerx, surface_rect.top))
            self.rendered_objs.append([surface, surface_rect])
        
        # Roll efficiency
        self.font.align= pygame.FONT_CENTER
        lst = rune.substats_efficiency
        if rune.innate_efficiency:
          lst = [*rune.innate_efficiency, *rune.substats_efficiency]
        lst = [str(value)+'%' for value in lst]
        roll_efficiency = "\n".join(lst)
        roll_efficiency = self.font.render(roll_efficiency,True,self.text_color,)
        roll_efficiency_rect = roll_efficiency.get_rect(
            midtop=(START_GRID["roll_efficiency"].centerx, surface_rect.top))
        self.rendered_objs.append([roll_efficiency, roll_efficiency_rect])

    def dispatch_events(self, e):
        for box in self.text_boxes.values():
            box.dispatch_events(e)
        
        for box in reversed(self.list_boxes.values()):
            box.dispatch_events(e)

        for button in self.buttons.values():
            button.dispatch_events(e)
            
        if e.type == pygame.QUIT:
            self.running = False
         
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.app.next_state('main_menu', self.persist)
                self.app.set_window('main_menu', True)
            if e.key == pygame.K_LCTRL:
                self.update_boxes(self.rune_obj)

    def update(self, dt):
        if not self.imgs:
            self.load_images()
            
        screenshot = PilIg.grab(all_screens=False)
        
        # Convert pil to cv2
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        if self.tesseract.data_thread is None and self.tesseract.text_thread is None:
            self.processing_image(image)

        self.tesseract.update(self.tese_images)
        data = self.tesseract.parse_data()
        self.rune_obj = Rune.from_dict(data)
        self.render(self.rune_obj)
            
        for box in self.text_boxes.values():
            box.update()
        
        for box in reversed(self.list_boxes.values()):
            box.update()
                
        for button in self.buttons.values():
            button.update()
            
    def draw(self, screen):
        # Bg color
        screen.fill(START_BG_COLOR) 
        
        for button in self.buttons.values():
            button.draw(screen)

        for box in self.text_boxes.values():
            box.draw(screen)
        
        for box in reversed(self.list_boxes.values()):
            box.draw(screen)
            
        for obj, pos in self.rendered_objs:
            screen.blit(obj, pos)
        
        try:
            for key in ('grade', 'substats_grade'):
                pygame.draw.rect(
                    screen,
                    RUNE_GRADES[getattr(self.rune_obj, key).lower()].color_fill,
                    START_GRID[key]
                    )
                
                screen.blit(
                    RUNE_GRADES[getattr(self.rune_obj, key).lower()].surface,
                    RUNE_GRADES[getattr(self.rune_obj, key).lower()].surface.get_rect(center=START_GRID[key].center)
                    )
        except KeyError:
            pass
            
        # Border Lines surface, color, start_pos, end_pos, width=1) 
        pygame.draw.rect(screen, "White", pygame.Rect((0, 0), DISPLAY_SIZES['rune_manager']), 2, 1)
        pygame.draw.line(screen, "White", (598, 650), (598, 0), 2)
        
        screen.blit(self.imgs['violent'], (620, 5))
        
        # Side grid
        for grid in START_GRID.values():
            pygame.draw.rect(screen, "White", grid, 2, 1)