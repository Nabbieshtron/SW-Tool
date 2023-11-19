import pygame

from constants import TEXT_BOX_FONT, TEXT_BOX_BORDER_COLORS

class TextBox:
    def __init__(self, dimensions:tuple[int], text:str):
        self.pos = dimensions[:2]
        self.size = dimensions[2:]
        self.box = pygame.Rect(dimensions)
        self.text = text
        
        self.active = False
        self.rendered_objs = []
        
        self.color = TEXT_BOX_BORDER_COLORS[0]
    
    def dispatch_event(self, e):
        self.color = TEXT_BOX_BORDER_COLORS[1] if self.active else TEXT_BOX_BORDER_COLORS[0]

        if e.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.box.collidepoint(e.pos)
            
        if e.type == pygame.KEYDOWN:
            if self.active:
                if e.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif not e.key == pygame.K_RETURN and len(self.text) < 3:
                    if e.unicode == '.' and self.text.count('.') == 0 and len(self.text) == 1:
                        self.text += e.unicode
                    if e.unicode.isdigit():
                        self.text += e.unicode
                    if len(self.text) == 1 and self.text.count('.') == 0:
                        self.text += '.'
            if e.key == pygame.K_RETURN:
                if self.active:
                    self.active = False
        
    def render(self):
        text_obj = TEXT_BOX_FONT.render(self.text, True, "Black")
        position = text_obj.get_rect(center=self.box.center)
        self.rendered_objs = (text_obj, position)
        
    def update(self):
        # Default max value
        if self.text and float(self.text) > 3.0:
            self.text = '3.0'
        if not self.active and len(self.text) == 2:
            self.text += '0'
        
        self.render()
      
    def draw(self, screen):
        screen.blit(*self.rendered_objs)
        
        pygame.draw.rect(screen, self.color, self.box, 2, 1)