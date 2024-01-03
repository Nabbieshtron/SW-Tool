import pygame
from dataclasses import dataclass, field
from typing import Self
from constants import (
    GRIND_MANAGER_FONT,
    GRIND_MANAGER_RECTS,
    START_BG_COLOR, 
)

class ActivatableComponent:
    # You need Python >=3.11 to use this typehint. If you're on 3.10 or below use Optional["ActivatableComponent"] instead
    active_component: Self | None = None

    def activate(self):
        ActivatableComponent.active_component = self

    def deactivate(self):
        if ActivatableComponent.active_component is self:
            ActivatableComponent.active_component = None
            
    # def update(self):
        # if ActivatableComponent.active_component is self:
            # do whatever


@dataclass
class ListBox(ActivatableComponent):
    color_menu: list[str]
    color_option: list[str]
    rect: pygame.Rect
    font: pygame.Font
    options : list[str]
    amount_showed: int
    main: str = ''
    draw_menu: bool = field(init=False, default=False)
    menu_active: bool = field(init=False, default=False)
    active_option: int = field(init=False, default=-1)
    mscroll_y: int = field(init=False, default=0)
    
    def dispatch_events(self, e):
        if e.type == pygame.MOUSEWHEEL and self.draw_menu:
            # Only works if amount_showed elements in list
            if len(self.options) > self.amount_showed and abs(self.mscroll_y) < (len(self.options)-self.amount_showed):
                # Capping how much is scrolled, e.y returns value depending how fast wheel is moved
                if e.y < 0:
                    self.mscroll_y -=1
                else:
                    self.mscroll_y +=1
            
            # If List end is reached only allows to go up
            if abs(self.mscroll_y) == (len(self.options)-self.amount_showed) and e.y > 0:
                self.mscroll_y +=1
                
            # Blocking scrolling upwards
            if self.mscroll_y > 0:
                self.mscroll_y = 0
            
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos) and ActivatableComponent.active_component is None:
                self.mscroll_y = 0
                self.draw_menu = not self.draw_menu
                ActivatableComponent.activate(self)
            elif self.draw_menu and self.active_option >= 0:
                self.mscroll_y = 0
                self.draw_menu = False
                ActivatableComponent.deactivate(self)
                self.main = self.options[self.active_option]

    def update(self):
        if ActivatableComponent.active_component is self:
            mpos = pygame.mouse.get_pos()
            self.menu_active = self.rect.collidepoint(mpos)
        
            self.active_option = -1
            for i in range(len(self.options)):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                if rect.collidepoint(mpos):
                    self.active_option = i+abs(self.mscroll_y)
                    break

            if not self.menu_active and self.active_option == -1:
                ActivatableComponent.deactivate(self)
                self.draw_menu = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_menu[self.menu_active], self.rect)
        pygame.draw.rect(screen, 'Black', self.rect, 2, 1)
        
        if self.main in self.options:
            msg = self.font.render(self.main, 1, 'Black')
            screen.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options[abs(self.mscroll_y):self.amount_showed+abs(self.mscroll_y)]):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(screen, self.color_option[1 if i+abs(self.mscroll_y) == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                screen.blit(msg, msg.get_rect(center = rect.center))


'''
-Arguments-
font: pygame.Font object
rect: pygame.Rect object
color_active: tuple that has 2 colors, (passive, active)
color_menu: tuple that has 2 colors, (passive, active)
char_type: allowed character type, type = ANY, DIGIT, ALPHABETIC. Default type ANY.
char_limit: allowed character limit. Default limit 0, unlimited.

-States-
menu_active: active when mouse collide with widget
box_active: widget active when left mouse pressed
guide_active: char_type error, upon active user gets pop up

-Other-
pop_up_rect: pygame.Rect object
'''

# For unlimited characters need to implement moving rect while writing
@dataclass
class TextBox(ActivatableComponent):
    font: pygame.Font
    rect: pygame.Rect
    color_active: tuple[str]
    color_menu: tuple[str]
    main: str = ''
    char_type: str = 'ANY'
    char_limit: int = 0
    menu_active: bool = False
    box_active: bool = False
    pop_up_timer: int = 0
    pop_up_object: tuple = field(default_factory=tuple)
    text_object: tuple = field(default_factory=tuple)
    
    def __post_init__(self):
        # Main text rendering
        text_surface = self.font.render(self.main, True, "Black")
        text_position = text_surface.get_rect(center=self.rect.center)
        self.text_object = (text_surface, text_position)
        
        # Guide text rendering
        self.pop_up_rect = self.rect.copy()
        self.pop_up_rect.bottom = self.rect.top + 20
        font = pygame.font.SysFont("Consolas", int(self.font.get_point_size()//1.7))
        text_surface = font.render(f'Only {self.char_type.lower()}', True, "Black")
        text_position = text_surface.get_rect(midtop=self.pop_up_rect.midtop)
        text_position.y += 4
        self.pop_up_object = (text_surface, text_position)
        
    def dispatch_events(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos) and ActivatableComponent.active_component is None:
                self.box_active = not self.box_active
                ActivatableComponent.activate(self)
                
        if e.type == pygame.KEYDOWN:
            if self.box_active:
                if e.key == pygame.K_BACKSPACE:
                    self.main = self.main[:-1]
                elif not e.key == pygame.K_RETURN:
                    if self.char_limit == 0 or len(self.main) < self.char_limit:
                        self.main += e.unicode
            if e.key == pygame.K_RETURN:
                if self.box_active:
                    self.box_active = False
                    self.pop_up_timer = self.type_check()
                    ActivatableComponent.deactivate(self)
                    
    def type_check(self):
        # Checkin main text type
        if self.char_type == 'DIGIT' and not self.main.isdigit():
            self.main = ''
            return 200
        elif self.char_type == 'FLOAT':
            try:
                self.main = str(float(self.main.replace(',', '.')))
            except ValueError:
                self.main = ''
                return 200
        return 0
        
    def update(self):
        if ActivatableComponent.active_component is self:
            mpos = pygame.mouse.get_pos()
            self.menu_active = self.rect.collidepoint(mpos)
            
        text_surface = self.font.render(self.main, True, "Black")
        text_position = text_surface.get_rect(center=self.rect.center)
        self.text_object = (text_surface, text_position)
        
        if self.pop_up_timer > 0:
            self.pop_up_timer -=1
            
    def draw(self, screen):
        if self.pop_up_timer > 0:
            pygame.draw.rect(screen, self.color_menu[self.menu_active], self.pop_up_rect)
            pygame.draw.rect(screen, self.color_active[self.box_active], self.pop_up_rect, 2, 10)
            screen.blit(*self.pop_up_object)
            
        pygame.draw.rect(screen, self.color_menu[self.menu_active], self.rect)
        pygame.draw.rect(screen, self.color_active[self.box_active], self.rect, 2, 1)
        screen.blit(*self.text_object)
