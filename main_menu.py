import pygame
import win32api
import win32con
import win32gui
from functools import partial

import user_config
from game_state import GameState
from windows import get_window_rect
from button import Button
from tesseract import Tesseract
from constants import (
    NAVIGATION_RECTANGLES_RECT,
    BG_COLOR, 
    NAVIGATION_RECTANGLE_COLOR,
    DEFAULT_CONFIGURATIONS,
    POSITION_INDICATOR_COLOR
)

class MainMenu(GameState):
    def __init__(self, app, persist, save_path):
        super().__init__(app, persist)
        self.app = app
        self.persist = persist
        self.ratios = None
        self.screen = None
        self.save_path = save_path
        
        # If positions of an app wasnt set the start button wont work
        self.is_set = DEFAULT_CONFIGURATIONS['is_set']
        self.indicator_color = POSITION_INDICATOR_COLOR
        
        # Rectangle visibility on/off
        self.navigation_boxes_state = DEFAULT_CONFIGURATIONS['navigation_boxes']

        # Rectangles
        self.transparent_rect = pygame.Rect(110, 10, 480, 340)
        self.navigation_rects = NAVIGATION_RECTANGLES_RECT
        
        self.buttons = {
            'rune_manager': Button(
                text='Start', 
                font=pygame.font.SysFont('Arial', 30),
                rect=pygame.Rect(5, 15, 100, 35),
                method=partial(self.next_state, 'rune_manager'),
                elevation=6,
                top_color="#475F77",
                bottom_color="#354B5E",
                text_color="#FFFFFF",
                collide_color="#D74B4B"
            ),
            'grind_manager': Button(
                text='Manage', 
                font=pygame.font.SysFont('Arial', 30),
                rect=pygame.Rect(5, 70, 100, 35),
                method=partial(self.next_state, 'grind_manager'),
                elevation=6,
                top_color="#475F77",
                bottom_color="#354B5E",
                text_color="#FFFFFF",
                collide_color="#D74B4B"
            ),
            'settings': Button(
                text='Settings', 
                font=pygame.font.SysFont('Arial', 30),
                rect=pygame.Rect(5, 125, 100, 35),
                method=partial(self.next_state, 'settings'),
                elevation=6,
                top_color="#475F77",
                bottom_color="#354B5E",
                text_color="#FFFFFF",
                collide_color="#D74B4B"
            ),
            'exit': Button(
                text='Exit', 
                font=pygame.font.SysFont('Arial', 30),
                rect=pygame.Rect(5, 180, 100, 35),
                method=partial(self.next_state, 'exit'),
                elevation=6,
                top_color="#475F77",
                bottom_color="#354B5E",
                text_color="#FFFFFF",
                collide_color="#D74B4B"
            ),
        }
        
    def next_state(self, state):
        if (state == "rune_manager" and self.persist.get('is_set', self.is_set)) or state in ("settings", "grind_manager"):
            self.app.next_state(state, self.persist)
            if state == 'grind_manager':
                self.app.set_window(state, True)
            else:
                self.app.set_window(state)

        elif state == 'exit':
            self.running = False
        
    def dispatch_events(self, e):
        if self.screen is None: 
            self.screen = self.app.screen.get_rect()
            
        # Buttons events
        for button in self.buttons.values():
            button.dispatch_events(e)
        
        # Set position on RETURN
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            self.persist['is_set'] = True
            self.persist['window_rect_attribute'] = get_window_rect()
            self.persist['navigation_rect_attributes'] = self.navigation_rects
            self.persist['transparent_rect'] = self.transparent_rect
            config = self.get_configurations()
            self.persist.update(config)
            user_config.save_settings(config, self.save_path)
            
        if (e.type == pygame.QUIT or
                e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            self.running = False
            
        if e.type == pygame.VIDEORESIZE:
            self.screen.w = 360 if e.w < 360 else e.w
            self.screen.h = 170 if e.h < 170 else e.h
            
            # Limiting resizing size
            if self.screen.w == 360 or self.screen.h == 170:
                pygame.display.set_mode((self.screen.w, self.screen.h), pygame.RESIZABLE)
    
    def get_configurations(self):
        keys = ('window_rect_attribute', 'navigation_rect_attributes', 'transparent_rect')
        dim_type = ('pos_x', 'pos_y', 'width', 'height')
        output = {}
        
        output['is_set'] = self.persist.get('is_set', self.is_set)
        
        if self.persist.get('is_set', self.is_set):
            output['window_rect_attribute'] = {key:dim for key, dim in zip(dim_type, self.persist['window_rect_attribute'])}
            output['transparent_rect'] = {key:dim for key, dim in zip(dim_type, self.persist['transparent_rect'])}
            output['navigation_rect_attributes'] = {
                key: {key:dim for key, dim in zip(dim_type, value)}
                for key, value in self.persist["navigation_rect_attributes"].items()
            }

        return output
        
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
        
        self.indicator_color = "Green" if self.persist.get('is_set', self.is_set) else "Red"

        for button in self.buttons.values():
            button.update()

    def draw(self, screen):
        screen.fill(BG_COLOR)

        # Draw transparent window
        pygame.draw.rect(screen, (255, 0, 128), self.transparent_rect)
        
        # Temp thing, update in future
        pygame.draw.rect(screen, self.indicator_color, self.transparent_rect, 2)
        
        for button in self.buttons.values():
            button.draw(screen)
        
        if self.persist.get('navigation_boxes', self.navigation_boxes_state):
            for key in ("title", "main", "innate", "substats", "grade"):
                    pygame.draw.rect(screen, NAVIGATION_RECTANGLE_COLOR, self.navigation_rects[key], 2)