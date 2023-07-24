import json
import pathlib

import constants
from button import Button


class Settings:
    def __init__(self, main_menu, program):
        self.main_menu = main_menu
        self.program = program
        self.cwd = pathlib.Path().absolute() / "settings.json"
        self.max_multiplier = 3
        self.min_multiplier = 0
        self.buttons = {
            key: Button(
                constants.BUTTON_NAMES[key],
                constants.BUTTON_POSITIONS[key],
                constants.BUTTON_SIZE["settings"],
            )
            for key in (
                "asset_type",
                "hide_or_show",
                "apply_changes",
                "cancel_changes",
            )
        }
        self.buttons.update(
            {
                key: Button(
                    constants.BUTTON_NAMES[key],
                    constants.BUTTON_POSITIONS[key],
                    constants.BUTTON_SIZE["eff_multipliers"],
                )
                for key in (
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
            }
        )

        # Loading saves
        self.load()

        self.saves = {
            key: self.buttons[key].text.lower()
            for key in self.buttons
            if key not in ("apply_changes", "cancel_changes")
        }

    def apply_changes(self):
        # Settings preferences
        self.saves = {
            key: self.buttons[key].text.lower()
            for key in self.buttons
            if key not in ("apply_changes", "cancel_changes")
        }

        # Applying the changes
        self.program.state = self.saves["asset_type"]
        self.main_menu.state = self.saves["asset_type"]
        self.main_menu.show = self.saves["hide_or_show"]

        # Save changes to json
        self.save()

    def save(self):
        # Save json file
        with open(self.cwd, "w") as settings:
            json.dump(self.saves, settings, indent=4)

    def load(self):
        # Load json file
        with open(self.cwd, "r") as settings:
            try:
                self.saves = json.load(settings)
            except json.JSONDecodeError:
                self.save()

        for key, value in self.saves.items():
            if key == "hide_or_show":
                self.buttons[key].flip_text = value == "show"
                self.main_menu.show = value
            elif key == "asset_type":
                self.buttons[key].flip_text = value == "rune"
                self.main_menu.state = value
                self.program.state = value
            else:
                self.buttons[key].text = value

    # Increase number showed on buttons
    def button_increase(self, key, increment):
        # Button name -> str(float)
        text = self.buttons[key].text
        num = float(text)

        # Checking the boundaries
        if num < self.max_multiplier:
            num = round(num + increment, 1)
            self.buttons[key].text = str(num)

    # Decrease number showed on buttons
    def button_decrease(self, key, decrement):
        # Button name -> str(float)
        text = self.buttons[key].text
        num = float(text)

        # Checking the boundaries
        if num > self.min_multiplier:
            num = round(num - decrement, 1)
            self.buttons[key].text = str(num)

    def draw(self, surface):
        surface.fill(constants.BG_COLOR)
        for key in constants.SETTINGS_TEXT_RECTS:
            surface.blit(
                constants.SETTINGS_TEXT_SURFACES[key],
                constants.SETTINGS_TEXT_RECTS[key],
            )

        for key, value in self.buttons.items():
            value.draw(surface)
            if key in (
                "asset_type",
                "hide_or_show",
                "apply_changes",
                "cancel_changes",
            ):
                value.button_effects()
            else:
                value.button_effects(right_click=True)

            if key == "asset_type":
                value.text_effect("Artifact")
            elif key == "hide_or_show":
                value.text_effect("Hide")
