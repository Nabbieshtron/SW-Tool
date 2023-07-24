import pygame

from constants import (
    DISPLAY_ARTIFACT,
    DISPLAY_MAIN_MENU,
    DISPLAY_RUNE,
    DISPLAY_SETTINGS,
    STATES,
)


class Display_handler:
    def __init__(self, app_handler):
        self.app_handler = app_handler
        self.screen = None
        self.set_display_mode()

    def set_display_mode(self):
        # Main menu
        if self.app_handler.status == STATES.MENU:
            self.screen = pygame.display.set_mode(DISPLAY_MAIN_MENU, pygame.RESIZABLE)
        # Main menu > Settings
        elif self.app_handler.status == STATES.SETTINGS:
            self.screen = pygame.display.set_mode(DISPLAY_SETTINGS)
        # Set ('rune' in settings)
        elif (
            self.app_handler.status == STATES.INAPP
            and self.app_handler.main_menu.state == "rune"
        ):
            self.screen = pygame.display.set_mode(DISPLAY_RUNE)
        # Set ('artifact' in settings)
        elif (
            self.app_handler.status == STATES.INAPP
            and self.app_handler.main_menu.state == "artifact"
        ):
            self.screen = pygame.display.set_mode(DISPLAY_ARTIFACT)

    def update(self):
        if self.app_handler.status == STATES.MENU:
            self.app_handler.main_menu.draw(self.screen)
        elif self.app_handler.status == STATES.INAPP:
            self.app_handler.program.draw(self.screen)
        elif self.app_handler.status == STATES.SETTINGS:
            self.app_handler.settings.draw(self.screen)
