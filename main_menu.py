from pygame.locals import Rect
import pygame
import button
import rects
import win32gui
import win32con
import win32api


class Main_menu:
    def __init__(self):
        self.bg_color: tuple[int] = (168, 148, 95)
        self.show = "show"
        self.state = "rune"

        # Button
        self.elevation = 6
        self.button_font = pygame.font.SysFont("Arial", 30)

        self.rects = {}

        self.rune_rects = {
            "title_rect": rects.Rects(Rect(170, 20, 360, 50)),
            "main_rect": rects.Rects(Rect(210, 0, 200, 50)),
            "inate_rect": rects.Rects(Rect(210, 0, 200, 45)),
            "sub_rect": rects.Rects(Rect(120, 0, 200, 130)),
        }

        self.artifact_rects = {
            "title_rect": rects.Rects(Rect(170, 20, 360, 50)),
            "main_rect": rects.Rects(Rect(210, 0, 150, 50)),
            "inate_rect": rects.Rects(Rect(210, 0, 200, 45)),
            "sub_rect": rects.Rects(Rect(120, 0, 330, 140)),
        }

        self.buttons = {
            "button_set": button.Button(
                "#475F77",
                "#354B5E",
                "Set",
                self.button_font,
                (5, 16),
                (100, 35),
                self.elevation,
            ),
            "button_settings": button.Button(
                "#475F77",
                "#354B5E",
                "Settings",
                self.button_font,
                (5, 70),
                (100, 35),
                self.elevation,
            ),
            "button_exit": button.Button(
                "#475F77",
                "#354B5E",
                "Exit",
                self.button_font,
                (5, 125),
                (100, 35),
                self.elevation,
            ),
        }

    @staticmethod
    def transparent_window():
        transparency_color = (255, 0, 128)

        # Create layered window
        hmwd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(
            hmwd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hmwd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(
            hmwd, win32api.RGB(*transparency_color), 0, win32con.LWA_COLORKEY
        )

        return transparency_color

    def update(self):
        if self.state == "rune":
            self.rects = self.rune_rects
        else:
            self.rects = self.artifact_rects

        # Get current mouse pos
        self.mouse_pos = button.get_mouse_pos()

        # Screen size
        self.width, self.height = pygame.display.get_window_size()

        # Transparent screen
        rects.Rects.transparent_rect.w = self.width - 120
        rects.Rects.transparent_rect.h = self.height - 20

        # Rects
        self.rects["title_rect"].get_scaled_rect()

        self.rects["main_rect"].get_scaled_rect()
        self.rects["main_rect"].rect.top = self.rects["title_rect"].rect.bottom - 2

        self.rects["inate_rect"].get_scaled_rect()
        self.rects["inate_rect"].rect.top = self.rects["main_rect"].rect.bottom - 2

        self.rects["sub_rect"].get_scaled_rect()
        self.rects["sub_rect"].rect.top = self.rects["inate_rect"].rect.bottom - 2

    def draw(self, screen):
        # Fill the surface
        screen.fill(self.bg_color)

        # Make window transparent
        self.transparency_color: tuple[int] = self.transparent_window()

        # Border filling
        pygame.draw.rect(screen, self.transparency_color, rects.Rects.transparent_rect)

        # Button
        self.buttons["button_set"].button_effects()
        self.buttons["button_settings"].button_effects()
        self.buttons["button_exit"].button_effects()

        self.buttons["button_set"].draw(screen)
        self.buttons["button_settings"].draw(screen)
        self.buttons["button_exit"].draw(screen)

        if self.show == "show":
            if self.state == "rune":
                # Rune name, level, slot
                self.rects["title_rect"].draw(screen)
                # Main-stat
                self.rects["main_rect"].draw(screen)
                # Inate-stat
                self.rects["inate_rect"].draw(screen)
                # Sub-stat
                self.rects["sub_rect"].draw(screen)
            else:
                # Artifact name, level
                self.rects["title_rect"].draw(screen)
                # Main-stat
                self.rects["main_rect"].draw(screen)
                # Sub-stat
                self.rects["sub_rect"].draw(screen)
