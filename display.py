from app_handler import App_handler
import pygame


class Display_handler:
    def __init__(self, app_handler):
        self.app_handler = app_handler
        self.screen = None
        self.set_display_mode()

    def set_display_mode(self):
        if self.app_handler.status == App_handler.status.MENU:
            self.screen = pygame.display.set_mode((600, 360), pygame.RESIZABLE)
        elif (
            self.app_handler.status == App_handler.status.INAPP
            and self.app_handler.main_menu.state == "rune"
            or self.app_handler.status == App_handler.status.SETTINGS
        ):
            self.screen = pygame.display.set_mode((600, 600))
        elif (
            self.app_handler.status == App_handler.status.INAPP
            and self.app_handler.main_menu.state == "artifact"
        ):
            self.screen = pygame.display.set_mode((900, 400))

    def update(self):
        if self.app_handler.status == App_handler.status.MENU:
            self.app_handler.main_menu.draw(self.screen)
        elif self.app_handler.status == App_handler.status.INAPP:
            self.app_handler.program.draw(self.screen)
        elif self.app_handler.status == App_handler.status.SETTINGS:
            self.app_handler.settings.draw(self.screen)
