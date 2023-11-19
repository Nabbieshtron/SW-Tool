import pygame

class Button:
    def __init__(
        self,
        rect,
        elevation,
        text,
        font,
        text_color,
        bg_colors,
        hover_color,
        method = lambda: None,
    ):
        self.top_rect = rect
        self.bottom_rect = rect.copy()
        self.font = font
        self.func = method
        
        self.dynamic_elevation = elevation
        self.original_pos_y = rect.y
        self.bg_colors = bg_colors
        self.text = text
        
        self.top_color = self.bg_colors[0]
        self.bottom_color = self.bg_colors[1]
        self.text_color = text_color
        self.hover_color = hover_color
        

        self.text_surf = None
        self.text_pos = None

        self.is_pressed = False
        
    def dispatch_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and self.top_rect.collidepoint(e.pos):
                self.is_pressed = True
                self.dynamic_elevation = 0
            else:
                self.is_pressed = False

        elif e.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed and self.top_rect.collidepoint(e.pos):
                self.func()
            self.dynamic_elevation = 6
            self.is_pressed = False
        
    def set_title(self, text):
        self.text = text
        
    def rendering(self):
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_pos = self.text_surf.get_rect(center=self.top_rect.center)
        
    def update(self):
        # Elevation logic
        self.top_rect.y = self.original_pos_y - self.dynamic_elevation
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        
        # Hover effect. Note!!! event loop pygame.MOUSEMOTION only works when mouse is moving
        if self.top_rect.collidepoint(pygame.mouse.get_pos()):
            self.top_color = self.hover_color
        elif not self.is_pressed:
            self.top_color = self.bg_colors[0]
            
        self.rendering()
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius = 7)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=7)
        
        screen.blit(
            self.text_surf,
            self.text_pos,
        )

