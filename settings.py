import pygame
import constants
from button import Button


class Settings:
    def __init__(self, main_menu, program):
        self.main_menu = main_menu
        self.program = program

        self.buttons = {
            key: Button(
                constants.BUTTON_NAMES[key],
                constants.BUTTON_POSITIONS[key],
                constants.BUTTON_SIZE["settings"],
            )
            for key in ("asset_type", "hide_or_show", "apply_changes", "cancel_changes")
        }

        self.changes = {
            "hide_or_show": self.buttons["hide_or_show"].text.lower(),
            "asset_type": self.buttons["asset_type"].text.lower(),
        }

    def apply_changes(self):
        for key, value in self.changes.items():
            if key == "asset_type":
                self.program.state = value
                self.main_menu.state = value
            elif key == "hide_or_show":
                self.main_menu.show = value

    def current_changes(self):
        for key, value in self.changes.items():
            if key == "hide_or_show":
                self.buttons[key].flip_text = True if value == "show" else False
            elif key == "asset_type":
                self.buttons[key].flip_text = True if value == "rune" else False

    def draw(self, surface):
        surface.fill(constants.BG_COLOR)
        for key in ("assets", "navsquares"):
            surface.blit(
                constants.SETTINGS_TEXT_SURFACES[key],
                constants.SETTINGS_TEXT_RECTS[key],
            )

        for key, value in self.buttons.items():
            value.draw(surface)
            value.button_effects()
            if key == "asset_type":
                value.text_effect("Artifact")
            elif key == "hide_or_show":
                value.text_effect("Hide")
