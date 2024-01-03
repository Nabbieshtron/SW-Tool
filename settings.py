import pygame
import json
import pathlib
from functools import partial

import user_config
from game_state import GameState
from button import Button
from widgets import TextBox
from constants import (
    BG_COLOR, 
    SETTINGS_BLIT,
    TEXT_BOX_COLOR,
    TEXT_BOX_FONT,
    SUB_VALUES
)


class Settings(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.perist = persist
        self.rendered_objs = SETTINGS_BLIT
        self.active_text_box = None
        
        # Path
        self.save_path = save_path
        
        # Efficiency multiplier default min and max values
        self.efficiency_multiplier_max = 3.0
        self.efficiency_multiplier_min = 0

        self.buttons = {}
        for n, (key, text) in enumerate(
            (
                ("assets", "Rune"),
                ("navigation_boxes", "True"),
                ("efficiency_default_value", "True"),
                ("apply", "Apply"),
                ("cancel", "Cancel"),
            )
        ):
            rect = 400, 20 + (60 * n), 150, 35
            if key == 'apply':
                rect = 325, 650, 150, 35
            if key == 'cancel':
                rect = 525, 650, 150, 35
                
            self.buttons[key] = Button(
                text=text,
                font=pygame.font.SysFont("Arial", 30),
                rect=pygame.Rect(rect),
                method=partial(self.on_press, key),
                elevation=6,
                top_color="#475F77",
                bottom_color="#354B5E",
                text_color="#FFFFFF",
                collide_color="#D74B4B",
            )
        
        self.text_boxes = {}
        text = '0.5'
        for n, key in enumerate(SUB_VALUES):
            if n > 2:
                text = '1.0'
                
            self.text_boxes[key] = TextBox(
                main=text,
                font=TEXT_BOX_FONT,
                rect=pygame.Rect(850, 75+(50*n), 100, 40),
                color_active=TEXT_BOX_COLOR,
                color_menu=['Pink', 'Light pink'],
                char_type='FLOAT',
                char_limit=3,
                )

    def on_press(self, key):
        if key == 'assets':
            if self.buttons[key].text == 'Rune':
                self.buttons[key].set_title('Artifact')
            else:
                self.buttons[key].set_title('Rune')
        elif key == 'navigation_boxes':
            if self.buttons[key].text == 'True':
                self.buttons[key].set_title('False')
            else:
                self.buttons[key].set_title('True')
        elif key == 'efficiency_default_value':
            if self.buttons[key].text == 'True':
                self.buttons[key].set_title('False')
            else:
                self.buttons[key].set_title('True')
        elif key == 'apply':
            configs = self.get_configurations()
            user_config.save_settings(configs, self.save_path)
            self.persist.update(configs)
            self.app.next_state("main_menu", self.persist)
            self.app.set_window('main_menu', True)
        elif key == 'cancel':
            # user_config.load_settings(self.save_path)
            self.app.next_state('main_menu', self.persist)
            self.app.set_window('main_menu', True)
        else:
            pass
            
    def get_configurations(self):
        preferences = {}

        # Assets state : Rune, Artifact
        preferences['assets'] = self.buttons['assets'].text
        
        # Navigation boxes state : True or False
        state = self.buttons['navigation_boxes'].text == 'True'
        preferences['navigation_boxes'] = state
        
        # Efficiency multipliers : dict[str:str]
        preferences['efficiency_multipliers'] = {
            key: tbox.main for key, tbox in self.text_boxes.items()
        }
        
        # Efficiency default value state : True or False
        state = self.buttons['efficiency_default_value'].text == 'True'
        preferences['efficiency_default_value'] = state

        return preferences

    def dispatch_events(self, e):
        # Buttons events
        for button in self.buttons.values():
            button.dispatch_events(e)

        for tbox in self.text_boxes.values():
            tbox.dispatch_events(e)
 
        if e.type == pygame.QUIT:
            self.running = False
            
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.app.next_state('main_menu', self.persist)
                self.app.set_window('main_menu', True)
                
    def update(self, dt):
        for button in self.buttons.values():
            button.update()
        
        for tbox in self.text_boxes.values():
            tbox.update()
        
    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        for tbox in self.text_boxes.values():
            tbox.draw(screen)
        
        for obj, pos in self.rendered_objs:
            screen.blit(obj, pos)
            
        for button in self.buttons.values():
            button.draw(screen)
