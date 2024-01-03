import pygame

from game_state import GameState
from widgets import ListBox, TextBox
from rune import RuneBox
from constants import (
    GRIND_MANAGER_FONT,
    GRIND_MANAGER_RECTS,
    START_BG_COLOR,
    RUNE_SETS,
    SUB_VALUES, 
) 
  
class GrindManager(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.persist = persist
        self.save_path = save_path
        self.rune_boxes = RuneBox.from_dict(self.persist['runes'])
            
    def dispatch_events(self, e):
        for rune_box in self.rune_boxes.values():
            rune_box.dispatch_events(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.app.next_state('main_menu', self.persist)
                self.app.set_window('main_menu', True)
        
    def update(self, dt):
        for key, rune_box in self.rune_boxes.items():
            rune_box.update()
            
    def draw(self, screen):
        screen.fill(START_BG_COLOR)
        
        for rune_box in self.rune_boxes.values():
            rune_box.draw(screen)
