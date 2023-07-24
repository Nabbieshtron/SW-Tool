import sys

import pygame

import window
from constants import STATES


class Event_handler:
    def __init__(self, app_handler, display_handler):
        self.app_handler = app_handler
        self.display_handler = display_handler
        self.sub_keys = (
            "HP_flat",
            "DEF_flat",
            "ATK_flat",
            "HP",
            "DEF",
            "ATK",
            "SPD",
            "CRI_Rate",
            "CRI_Damage",
            "Accuracy",
            "Resistance",
        )

    def video_resize(self):
        if self.app_handler.status == STATES.MENU:
            width, height = pygame.display.get_window_size()
            if width < 360:
                width = 360
            if height < 170:
                height = 170
            pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def key_down(self, key):
        if self.app_handler.status == STATES.MENU:
            if key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif self.app_handler.status == STATES.INAPP:
            if key == pygame.K_ESCAPE:
                self.app_handler.revert_status()
                self.app_handler.program.initialize = True
                self.display_handler.set_display_mode()
        elif self.app_handler.status == STATES.SETTINGS:
            if key == pygame.K_ESCAPE:
                self.app_handler.revert_status()
                self.display_handler.set_display_mode()

    def mouse_button_up(self, button):
        if self.app_handler.status == STATES.MENU:
            if button == 1:
                if self.app_handler.main_menu.BUTTONS["set"].collision_check():
                    self.app_handler.set_status(STATES.INAPP)
                    self.app_handler.program.image.rects = (
                        self.app_handler.main_menu.rects
                    )
                    self.app_handler.program.image.window_rect = pygame.Rect(
                        *window.get_size()
                    )
                    self.display_handler.set_display_mode()
                elif self.app_handler.main_menu.BUTTONS["settings"].collision_check():
                    self.app_handler.set_status(STATES.SETTINGS)
                    self.display_handler.set_display_mode()
                elif self.app_handler.main_menu.BUTTONS["exit"].collision_check():
                    pygame.quit()
                    sys.exit()
        elif self.app_handler.status == STATES.SETTINGS:
            if button == 1:
                if self.app_handler.settings.buttons["asset_type"].collision_check():
                    self.app_handler.settings.buttons["asset_type"].clicked = True

                elif self.app_handler.settings.buttons[
                    "hide_or_show"
                ].collision_check():
                    self.app_handler.settings.buttons["hide_or_show"].clicked = True

                elif self.app_handler.settings.buttons[
                    "apply_changes"
                ].collision_check():
                    self.app_handler.settings.apply_changes()
                    self.app_handler.revert_status()
                    self.display_handler.set_display_mode()

                elif self.app_handler.settings.buttons[
                    "cancel_changes"
                ].collision_check():
                    self.app_handler.settings.load()
                    self.app_handler.revert_status()
                    self.display_handler.set_display_mode()

                for key in self.sub_keys:
                    if self.app_handler.settings.buttons[key].collision_check():
                        self.app_handler.settings.button_increase(key, 0.1)

            elif button == 3:
                for key in self.sub_keys:
                    if self.app_handler.settings.buttons[key].collision_check():
                        self.app_handler.settings.button_decrease(key, 0.1)
