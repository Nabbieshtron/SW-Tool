import pygame

from dataclasses import dataclass

@dataclass
class Button:
    text: str
    font: pygame.font
    rect: pygame.Rect
    method: callable
    elevation: int
    top_color: str
    bottom_color: str
    text_color : str
    collide_color: str
    is_pressed: bool = False
    
    def __post_init__(self):
        self.dynamic_color = None
        self.original_pos_y = self.rect.y
        self.top_rect: pygame.Rect = self.rect.copy()
        self.bottom_rect: pygame.Rect = self.rect.copy()
        
    def dispatch_events(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and self.top_rect.collidepoint(e.pos):
                self.is_pressed = True
                self.elevation = 0
            else:
                self.is_pressed = False

        elif e.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.top_rect.collidepoint(e.pos):
                self.method()
            self.elevation = 6
            self.is_pressed = False

    def set_title(self, text):
        self.text = text

    def render(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)
        
    def update(self):
        # Elevation logic
        self.top_rect.y = self.original_pos_y - self.elevation
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation
        
        if self.top_rect.collidepoint(pygame.mouse.get_pos()):
            self.dynamic_color = self.collide_color
        elif not self.is_pressed:
            self.dynamic_color = self.top_color
        
        self.render()
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 7)
        pygame.draw.rect(screen, self.dynamic_color, self.top_rect, border_radius=7)
        
        screen.blit(
            self.text_surface,
            self.text_rect,
        )