from app_handler import App_handler
import window
import pygame
import sys


class Event_handler:
    def __init__(self, app_handler, display_handler):
        self.app_handler = app_handler
        self.display_handler = display_handler

    def video_resize(self):
        if self.app_handler.status == App_handler.status.MENU:
            width, height = pygame.display.get_window_size()
            if width < 360:
                width = 360
            if height < 170:
                height = 170
            pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def key_down(self, key):
        if self.app_handler.status == App_handler.status.MENU:
            if key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.app_handler.status == App_handler.status.INAPP:
            if key == pygame.K_ESCAPE:
                self.app_handler.revert_status()
                self.app_handler.program.initialize = True
                self.display_handler.set_display_mode()
        elif self.app_handler.status == App_handler.status.SETTINGS:
            if key == pygame.K_ESCAPE:
                self.app_handler.revert_status()
                self.display_handler.set_display_mode()

    def mouse_button_up(self, button):
        if self.app_handler.status == App_handler.status.MENU:
            if button == 1:
                if self.app_handler.main_menu.buttons["button_set"].collision_check():
                    self.app_handler.set_status(App_handler.status.INAPP)
                    self.app_handler.program.image.rects = (
                        self.app_handler.main_menu.rects
                    )
                    self.app_handler.program.image.window_rect = pygame.Rect(
                        *window.get_size()
                    )
                    self.display_handler.set_display_mode()
                elif self.app_handler.main_menu.buttons[
                    "button_settings"
                ].collision_check():
                    self.app_handler.set_status(App_handler.status.SETTINGS)
                    self.display_handler.set_display_mode()
                elif self.app_handler.main_menu.buttons[
                    "button_exit"
                ].collision_check():
                    pygame.quit()
                    sys.exit()
        elif self.app_handler.status == App_handler.status.SETTINGS:
            if button == 1:
                if self.app_handler.settings.buttons[
                    "game_asset_type"
                ].collision_check():
                    self.app_handler.settings.buttons["game_asset_type"].clicked = True
                elif self.app_handler.settings.buttons[
                    "hide_or_show"
                ].collision_check():
                    self.app_handler.settings.buttons["hide_or_show"].clicked = True
                elif self.app_handler.settings.buttons[
                    "apply_changes"
                ].collision_check():
                    self.app_handler.settings.changes[
                        "game_asset_type"
                    ] = self.app_handler.settings.buttons[
                        "game_asset_type"
                    ].text.lower()
                    self.app_handler.settings.changes[
                        "hide_or_show"
                    ] = self.app_handler.settings.buttons["hide_or_show"].text.lower()
                    self.app_handler.settings.apply_changes()
                    self.app_handler.revert_status()
                    self.display_handler.set_display_mode()
                elif self.app_handler.settings.buttons[
                    "cancel_changes"
                ].collision_check():
                    self.app_handler.settings.current_changes()
                    self.app_handler.revert_status()
                    self.display_handler.set_display_mode()
