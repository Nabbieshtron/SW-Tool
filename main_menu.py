import pygame
import win32api
import win32con
import win32gui
from functools import partial

from game_state import GameState
from windows import get_window_rect
from button import Button
from constants import (
    NAVIGATION_RECTANGLES_RECT,
    BUTTON_RECTS,
    BUTTON_TEXTS,
    ELEVATION,
    BACKGROUND_COLOR, 
    NAVIGATION_RECTANGLE_COLOR,
    BUTTON_FONT,
    BUTTON_TEXT_COLOR,
    BUTTON_BG_COLORS,
    BUTTON_HOVER_COLOR
)

from tesseract import Tesseract

class MainMenu(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.persist = persist
        self.ratios = None
        self.screen = None
        self.save_path = save_path
        
        # Rectangle visibility flag
        self.navigation_boxes = True

        # Rectangles
        self.transparent_rect = pygame.Rect(110, 10, 480, 340)
        self.navigation_rects = NAVIGATION_RECTANGLES_RECT
        
        self.buttons = {
            key: Button(
                BUTTON_RECTS[key], 
                ELEVATION,
                BUTTON_TEXTS[key],
                BUTTON_FONT,
                BUTTON_TEXT_COLOR,
                BUTTON_BG_COLORS,
                BUTTON_HOVER_COLOR,
                partial(self.next_state, key)
            )
            for key in ('start', 'settings', 'exit')
        }
        
        self.load_preferences()
        
    def next_state(self, state):
        if (
            state == "start" and self.persist["transparent_dim"]
        ) or state == "settings":
            self.app.next_state(state, self.persist)
            self.app.set_window(state)
        elif state == 'exit':
            self.running = False
        
    def dispatch_event(self, e):
        if self.screen is None: 
            self.screen = self.app.screen.get_rect()
            
        # Buttons events
        for button in self.buttons.values():
            button.dispatch_event(e)
        
        # Set position on RETURN
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            self.persist['window_dim_attribute'] = get_window_rect()
            self.persist['navigation_dims_attributes'] = self.navigation_rects
            self.persist['transparent_dim'] = self.transparent_rect
            self.app.save_to_disk(self.get_preferences(), self.save_path)
            
        if (e.type == pygame.QUIT or
                e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            self.running = False
            
        if e.type == pygame.VIDEORESIZE:
            self.screen.w = 360 if e.w < 360 else e.w
            self.screen.h = 170 if e.h < 170 else e.h
            
            # Limiting resizing size
            if self.screen.w == 360 or self.screen.h == 170:
                pygame.display.set_mode((self.screen.w, self.screen.h), pygame.RESIZABLE)
    
    def get_preferences(self):
        preferences = {}
        
        preferences['window_dim_attribute'] = tuple(self.persist['window_dim_attribute'])
        
        preferences['transparent_dim'] = tuple(self.persist['transparent_dim'])
        
        preferences['navigation_dims_attributes'] = {key:tuple(value) for key, value in self.persist['navigation_dims_attributes'].items()}
        
        return preferences
        
    def load_preferences(self):
         # Show or Hide nav box
        self.navigation_boxes = self.persist['navigation_boxes_state']
        
        
    def update(self, dt):
        # Collecting all the ratios of navigation rects
        if self.ratios is None:
            self.ratios = {key:(
                (_rect.x - self.transparent_rect.x) / self.transparent_rect.w,
                (_rect.y - self.transparent_rect.y) / self.transparent_rect.h,
                _rect.w / self.transparent_rect.w,
                _rect.h / self.transparent_rect.h,)
            for key, _rect in self.navigation_rects.items()
            }
            
        self.transparent_rect = pygame.Rect(110, 10, self.screen.w - 120 ,self.screen.h - 20)

        # Scaling the navigation rects by ratio
        for key, _rect in self.navigation_rects.items():
            _rect.x = self.ratios[key][0] * self.transparent_rect.w + self.transparent_rect.x
            _rect.y = self.ratios[key][1] * self.transparent_rect.h + self.transparent_rect.y
            _rect.w = self.ratios[key][2] * self.transparent_rect.w
            _rect.h = self.ratios[key][3] * self.transparent_rect.h
        
        self.navigation_rects["main"].top = self.navigation_rects["title"].bottom - 2
        self.navigation_rects["innate"].top = self.navigation_rects["main"].bottom - 2
        self.navigation_rects["substats"].top = self.navigation_rects["innate"].bottom - 2
        self.navigation_rects["grade"].top = self.navigation_rects["title"].bottom + 10
        
        hmwd = pygame.display.get_wm_info()["window"]
         
        # Create layered window
        win32gui.SetWindowLong(
            hmwd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hmwd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(
            hmwd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY
        )
        
        for button in self.buttons.values():
            button.update()

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)

        # Draw transparent window
        pygame.draw.rect(screen, (255, 0, 128), self.transparent_rect)
        
        # Temp thing, update in future
        c = "Green" if self.persist['transparent_dim'] else "Red"
        pygame.draw.rect(screen, c, self.transparent_rect, 2)
        
        for button in self.buttons.values():
            button.draw(screen)
        
        if self.navigation_boxes:
            for key in ("title", "main", "innate", "substats", "grade"):
                    pygame.draw.rect(screen, NAVIGATION_RECTANGLE_COLOR, self.navigation_rects[key], 2)