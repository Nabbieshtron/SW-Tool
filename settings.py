import pygame
import json
import pathlib
from functools import partial

from game_state import GameState
from button import Button
from text_box import TextBox
from constants import (
    BACKGROUND_COLOR, 
    SETTINGS_TEXTS_WITH_POS, 
    SETTINGS_FONT,
    BUTTON_RECTS,
    BUTTON_TEXTS,
    ELEVATION,
    BUTTON_FONT,
    BUTTON_TEXT_COLOR,
    BUTTON_BG_COLORS,
    BUTTON_HOVER_COLOR,
    EFFICIENCY_MULTIPLIERS_TEXT_BOXES_ATTRIBUTES,
    DEFAULT_EFFICIENCY_MULTIPLIER,
)


class Settings(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.perist = persist
        self.rendered_objs = []
        
        # Path
        self.save_path = save_path
        
        # Efficiency multiplier default min and max values
        self.efficiency_multiplier_max = 3.0
        self.efficiency_multiplier_min = 0
        
        self.buttons = {
            key: Button(
                BUTTON_RECTS[key], 
                ELEVATION,
                BUTTON_TEXTS[key],
                BUTTON_FONT,
                BUTTON_TEXT_COLOR,
                BUTTON_BG_COLORS,
                BUTTON_HOVER_COLOR,
                partial(self.on_press, key)
            )
            for key in (
                'assets',
                'navigation_boxes',
                'efficiency_default_value',
                'apply',
                'cancel'
            )
        }

        # Text boxes
        self.text_boxes = {
            tpl[0]: TextBox(EFFICIENCY_MULTIPLIERS_TEXT_BOXES_ATTRIBUTES[i], tpl[1])
            for i, tpl in enumerate(DEFAULT_EFFICIENCY_MULTIPLIER.items())
        }
        self.active_text_box = None
        
        # Load saves
        self.load_preferences()
        
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
            # Collecting new user preferences and saving to disk
            self.app.save_to_disk(self.get_preferences(), self.save_path)
            
            self.app.next_state("main_menu", self.perist)
            self.app.set_window('main_menu', True)
        elif key == 'cancel':
            self.load_preferences()
            self.app.next_state('main_menu', self.perist)
            self.app.set_window('main_menu', True)
        else:
            pass
            
    def get_preferences(self):
        preferences = {}

        # Assets state : Rune, Artifact
        preferences['assets_state'] = self.buttons['assets'].text
        
        # Navigation boxes state : True or False
        state = self.buttons['navigation_boxes'].text == 'True'
        preferences['navigation_boxes_state'] = state
        
        # Efficiency multipliers : dict[str:str]
        preferences['efficiency_multipliers'] = {
            key: tbox.text for key, tbox in self.text_boxes.items()
        }
        
        # Efficiency default value state : True or False
        state = self.buttons['efficiency_default_value'].text == 'True'
        preferences['efficiency_default_value'] = state
        
        # Update persist
        self.persist.update(preferences)
        return preferences
        
    def load_preferences(self):
        # Assets state : Rune, Artifact
        self.buttons['assets'].text = self.persist['assets_state']
        
        # Navigation boxes state : Show, Hide
        state = str(self.persist['navigation_boxes_state'])
        self.buttons['navigation_boxes'].text = state
        
        # Efficiency multipliers
        for key, value in self.persist['efficiency_multipliers'].items():
            self.text_boxes[key].text = value
        
        # Efficiency default value state : True or False
        state = str(self.persist['efficiency_default_value'])
        self.buttons['efficiency_default_value'].text = state

    def rendering(self):
        self.rendered_objs = []
        
        for _rect, text in SETTINGS_TEXTS_WITH_POS:
            text_obj = SETTINGS_FONT.render(text, True, "Black")
            
            # Set rect size
            _rect.size = text_obj.get_size()
            
            self.rendered_objs.append((text_obj, _rect))

    def dispatch_event(self, e):
        # Buttons events
        for button in self.buttons.values():
            button.dispatch_event(e)

        for tbox in self.text_boxes.values():
            tbox.dispatch_event(e)
 
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

        self.rendering()
        
    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        
        for tbox in self.text_boxes.values():
            tbox.draw(screen)
        
        for obj, pos in self.rendered_objs:
            screen.blit(obj, pos)
            
        for button in self.buttons.values():
            button.draw(screen)
