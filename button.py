from pygame.locals import Rect
import pygame
import win32gui


def get_mouse_pos():
    # get mouse position
    flags, hcursor, (x1, y1) = win32gui.GetCursorInfo()
    rect = win32gui.GetWindowRect(pygame.display.get_wm_info()["window"])
    titlebar_padding_x = rect[2] - rect[0] - pygame.display.get_window_size()[0]
    titlebar_padding_y = rect[3] - rect[1] - pygame.display.get_window_size()[1]
    pos_x = x1 - rect[0] - titlebar_padding_x // 2
    pos_y = y1 - rect[1] - titlebar_padding_y + titlebar_padding_x // 2
    return (pos_x, pos_y)


class Button:
    def __init__(self, color_top, color_bottom, text, font, position, size, elevation):
        self.pressed = False
        self.flip_text = True
        self.clicked = False

        self.color1 = color_top
        self.color2 = color_bottom

        self.font = font
        self.original_text = text
        self.text: str = text
        self.text_surf = 0

        self.pos: tuple = position
        self.size: tuple = size
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_pos_y = self.pos[1]

        self.top_rect = Rect((self.pos), (self.size))
        self.bottom_rect = Rect((self.pos), (self.size[0], self.elevation))
        self.text_rect = 0

    def collision_check(self):
        return self.top_rect.collidepoint(
            *get_mouse_pos()
        ) or self.bottom_rect.collidepoint(*get_mouse_pos())

    def button_effects(self):
        detect_press = pygame.mouse.get_pressed()[0]

        # Blinking effect
        self.color1 = "#D74B4B" if self.collision_check() else "#475F77"

        # Pressing effect
        if detect_press and not self.pressed:
            self.pressed = True
            self.dynamic_elevation = 0 if self.collision_check() else self.elevation

        if not detect_press:
            self.pressed = False
            self.dynamic_elevation = self.elevation

    def text_effect(self, text):
        # Text effect
        if self.collision_check():
            self.text = text if self.flip_text else self.original_text
            if self.clicked:
                self.clicked = False
                self.flip_text = False if self.flip_text else True

        else:
            self.text = self.original_text if self.flip_text else text

    def draw(self, surface):
        self.text_surf = self.font.render(self.text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        # Elevation logic
        self.top_rect.y = self.original_pos_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(surface, self.color2, self.bottom_rect, border_radius=12)
        pygame.draw.rect(surface, self.color1, self.top_rect, border_radius=12)
        surface.blit(self.text_surf, self.text_rect)
