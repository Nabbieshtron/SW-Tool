import pygame
import win32api
import win32con
import win32gui

from button import Button
from constants import (
    ARTIFACT_RECTS,
    BG_COLOR,
    BUTTON_NAMES,
    BUTTON_POSITIONS,
    BUTTON_SIZE,
    MENU_BORDER_COLOR,
    RUNE_RECTS,
    TRANSPARENCY_COLOR,
)
from rects import Rects


class Main_menu:
    def __init__(self):
        self.show = "show"
        self.state = "rune"

        self.rune_rects = {key: Rects(value) for key, value in RUNE_RECTS.items()}
        self.artifact_rects = {
            key: Rects(value) for key, value in ARTIFACT_RECTS.items()
        }

        # Buttons
        self.BUTTONS = {
            key: Button(
                BUTTON_NAMES[key],
                BUTTON_POSITIONS[key],
                BUTTON_SIZE["menu"],
            )
            for key in ("set", "settings", "exit")
        }

    def transparent_window(self):
        # Create layered window
        hmwd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(
            hmwd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hmwd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(
            hmwd, win32api.RGB(*TRANSPARENCY_COLOR), 0, win32con.LWA_COLORKEY
        )

    def update(self):
        if self.state == "rune":
            self.rects = self.rune_rects
        else:
            self.rects = self.artifact_rects

        # Screen size
        self.width, self.height = pygame.display.get_window_size()

        Rects.transparent_rect.w = self.width - 120
        Rects.transparent_rect.h = self.height - 20

        # Rects
        for key in ("title_rect", "main_rect", "inate_rect", "sub_rect"):
            self.rects[key].get_scaled_rect()

        self.rects["main_rect"].rect.top = self.rects["title_rect"].rect.bottom - 2
        self.rects["inate_rect"].rect.top = self.rects["main_rect"].rect.bottom - 2
        self.rects["sub_rect"].rect.top = self.rects["inate_rect"].rect.bottom - 2

        # Prepare transparent window
        self.transparent_window()

    def draw(self, screen):
        # Fill the surface
        screen.fill(BG_COLOR)

        # Draw transparent window
        pygame.draw.rect(screen, TRANSPARENCY_COLOR, Rects.transparent_rect)

        # Button
        for key in ("set", "settings", "exit"):
            self.BUTTONS[key].button_effects()
            self.BUTTONS[key].draw(screen)

        if self.show == "show":
            if self.state == "rune":
                for key in ("title_rect", "main_rect", "inate_rect", "sub_rect"):
                    self.rects[key].draw(screen, MENU_BORDER_COLOR)

            else:
                for key in ("title_rect", "main_rect", "sub_rect"):
                    self.rects[key].draw(screen, MENU_BORDER_COLOR)
