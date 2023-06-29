import pygame
import win32gui
import constants


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
    def __init__(self, text, position, size):
        self.pressed = False
        self.flip_text = True
        self.clicked = False

        self.original_text = text
        self.text: str = text

        self.color1 = "#475F77"
        self.pos: tuple = position
        self.size: tuple = size
        self.dynamic_elevation = constants.ELEVATION
        self.original_pos_y = self.pos[1]

        self.top_rect = pygame.Rect((self.pos), (self.size))
        self.bottom_rect = pygame.Rect((self.pos), (self.size[0], constants.ELEVATION))

    def collision_check(self):
        return self.top_rect.collidepoint(
            get_mouse_pos()
        ) or self.bottom_rect.collidepoint(get_mouse_pos())

    def button_effects(self):
        detect_press = pygame.mouse.get_pressed()[0]

        # Blinking effect
        self.color1 = (
            constants.BUTTON_EFFECT_ON_COLOR
            if self.collision_check()
            else constants.BUTTON_EFFECT_OFF_COLOR
        )

        # Pressing effect
        if detect_press and not self.pressed:
            self.pressed = True
            self.dynamic_elevation = (
                0 if self.collision_check() else constants.ELEVATION
            )

        if not detect_press:
            self.pressed = False
            self.dynamic_elevation = constants.ELEVATION

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
        text_surf = constants.BUTTON_FONT.render(
            self.text, True, constants.BUTTON_TEXT_COLOR
        )
        text_rect = text_surf.get_rect(center=self.top_rect.center)

        # Elevation logic
        self.top_rect.y = self.original_pos_y - self.dynamic_elevation
        text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(
            surface, constants.BUTTON_BOTTOM_COLOR, self.bottom_rect, border_radius=12
        )
        pygame.draw.rect(surface, self.color1, self.top_rect, border_radius=12)
        surface.blit(text_surf, text_rect)
