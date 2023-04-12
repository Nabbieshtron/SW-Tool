import pygame
import button


class Settings:
    def __init__(self, main_menu, program):
        self.bg_color: tuple[int] = (168, 148, 95)
        self.main_menu = main_menu
        self.program = program

        # Button
        self.elevation = 6
        self.font = pygame.font.SysFont("Ariel", 30)

        self.buttons = {
            "game_asset_type": button.Button(
                "#475F77",
                "#354B5E",
                "Rune",
                self.font,
                (400, 15),
                (150, 35),
                self.elevation,
            ),
            "hide_or_show": button.Button(
                "#475F77",
                "#354B5E",
                "Show",
                self.font,
                (400, 75),
                (150, 35),
                self.elevation,
            ),
            "apply_changes": button.Button(
                "#475F77",
                "#354B5E",
                "Apply",
                self.font,
                (150, 550),
                (140, 35),
                self.elevation,
            ),
            "cancel_changes": button.Button(
                "#475F77",
                "#354B5E",
                "Cancel",
                self.font,
                (300, 550),
                (160, 35),
                self.elevation,
            ),
        }

        self.changes = {
            "hide_or_show": self.buttons["hide_or_show"].text.lower(),
            "game_asset_type": self.buttons["game_asset_type"].text.lower(),
        }

        self.settings_surf = {
            "surf_1": self.font.render("Select game asset", True, "Black"),
            "surf_2": self.font.render("Navigation squares", True, "Black"),
        }

        self.settings_rect = {
            "rect_1": self.settings_surf["surf_1"].get_rect(topleft=(20, 20)),
            "rect_2": self.settings_surf["surf_2"].get_rect(topleft=(20, 80)),
        }

    def apply_changes(self):
        for key, value in self.changes.items():
            if key == "game_asset_type":
                self.program.state = value
                self.main_menu.state = value
            elif key == "hide_or_show":
                self.main_menu.show = value

    def current_changes(self):
        for key, value in self.changes.items():
            if key == "hide_or_show":
                self.buttons[key].flip_text = True if value == "show" else False
            elif key == "game_asset_type":
                self.buttons[key].flip_text = True if value == "rune" else False

    def draw(self, surface):
        surface.fill(self.bg_color)
        surface.blit(self.settings_surf["surf_1"], self.settings_rect["rect_1"])
        surface.blit(self.settings_surf["surf_2"], self.settings_rect["rect_2"])

        for key, value in self.buttons.items():
            value.draw(surface)
            value.button_effects()
            if key == "game_asset_type":
                value.text_effect("Artifact")
            elif key == "hide_or_show":
                value.text_effect("Hide")
