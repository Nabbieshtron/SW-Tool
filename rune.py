import pygame
from constants import (
    IN_APP_FONT,
    IN_APP_TEXT_COLOR,
    RUNE_SETS,
    RUNE_QUALITY_BG_COLORS,
    DEFAULT_RUNE_QUALITY,
    IN_APP_GRID,
    DISPLAY_RUNE,
)
from efficiency import Efficiency as Ef


class Rune:
    def __init__(self):
        self.efficiency = Ef()
        self.font = IN_APP_FONT
        # Tesseract data
        self.rune_data = {}

        # Rendered text
        self.render_data = {"subs": "", "roll_eff": ""}

        # Rect
        self.rect_data = {"subs": "", "roll_eff": ""}

    def render(self):
        # Cleaning for a loop
        self.render_data = {"subs": "", "roll_eff": ""}
        self.font.align = pygame.FONT_LEFT

        # Level, slot, name, main
        for key in ("level", "slot", "name", "main"):
            self.render_data[key] = self.font.render(
                " ".join(self.rune_data[key]), True, IN_APP_TEXT_COLOR
            )
        # Rune substats
        self.render_data["subs"] = self.font.render(
            "\n".join(
                n + " " + v for n, v in [x[:-1] for x in self.rune_data["subs"]]
            ).strip(),
            True,
            IN_APP_TEXT_COLOR,
        )
        # Rune grinds
        self.font.align = pygame.FONT_CENTER
        self.render_data["grinds"] = self.font.render(
            "\n".join(
                v.replace("+", "") for v in [x[-1] for x in self.rune_data["subs"]]
            ).strip(),
            True,
            IN_APP_TEXT_COLOR,
        )
        # Roll efficiency
        self.render_data["roll_eff"] = self.font.render(
            "\n".join(
                str(round(value)) + "%" for value in self.efficiency.ref.values()
            ),
            True,
            IN_APP_TEXT_COLOR,
        )

        # Rune efficiency
        self.render_data["rune_eff"] = (
            self.font.render(self.efficiency.rune_eff, True, IN_APP_TEXT_COLOR)
            if 12 <= int(self.rune_data["level"][0]) <= 15
            else self.font.render("N", True, IN_APP_TEXT_COLOR)
        )

    def creating_rect(self):
        # Cleaning for a loop
        self.rect_data = {"subs": "", "roll_eff": ""}

        # Level, slot
        for key in ("level", "slot"):
            self.rect_data[key] = self.render_data[key].get_rect(
                center=IN_APP_GRID[key].center
            )

        # Name, main
        y = 20
        for key in ("name", "main"):
            self.rect_data[key] = self.render_data[key].get_rect(midtop=(300, y))
            y += 40

        # Rune substats
        self.rect_data["subs"] = self.render_data["subs"].get_rect(topleft=(100, 170))

        # Rune grinds
        self.rect_data["grinds"] = self.render_data["grinds"].get_rect(
            midtop=(IN_APP_GRID["grinds"].centerx, self.rect_data["subs"].top)
        )

        # Roll efficiency
        self.rect_data["roll_eff"] = self.render_data["roll_eff"].get_rect(
            midtop=(IN_APP_GRID["roll_eff"].centerx, self.rect_data["subs"].top)
        )

        # Rune efficiency
        self.rect_data["rune_eff"] = self.render_data["rune_eff"].get_rect(
            center=IN_APP_GRID["rune_eff"].center
        )

    def preparing_data(self, data):
        try:
            # Removing empty elements
            data = [el for el in data if el]

            # Level
            self.rune_data["level"] = (
                [data.pop(0).replace("+", "")]
                if any(char.isnumeric() for char in data[0])
                else ["0"]
            )

            # Name
            self.rune_data["name"] = [
                data[:n] for n, x in enumerate(data) if r")" in x
            ][0]

            # Set
            name = [x.lower() for x in self.rune_data["name"]]
            for rune_set in RUNE_SETS:
                if rune_set in name:
                    self.rune_data["set"] = [rune_set]
                    break
            else:
                self.rune_data["set"] = ["N"]

            # Slot
            self.rune_data["slot"] = [
                (
                    data.pop(len(self.rune_data["name"]))
                    .replace("(", "")
                    .replace(")", "")
                )
            ]

            # Main
            self.rune_data["main"] = []
            for el in data[len(self.rune_data["name"]) :]:
                if any(char.isnumeric() for char in el):
                    self.rune_data["main"].append(el)
                    break
                else:
                    self.rune_data["main"].append(el)

            # Substat
            self.rune_data["subs"] = data[
                len(self.rune_data["name"]) + len(self.rune_data["main"]) :
            ]
            output = []
            new = ""
            for el in self.rune_data["subs"]:
                if "+" in el:
                    if el.count("+") >= 2:
                        x = ["+" + i for i in el.split("+") if i]
                        x.insert(0, new[:-1])
                        output.append(x)
                        new = ""
                    elif "%" not in el:
                        output.append([new, el, "N"])
                        new = ""
                    else:
                        output.append([new[:-1], el, "N"])
                        new = ""
                elif el.isalnum():
                    new += el + " "
            self.rune_data["subs"] = output
        except IndexError:
            self.rune_data = {
                "level": ["0"],
                "name": [],
                "slot": [],
                "main": [],
                "subs": [],
            }

    def update(self, data):
        # Preparing data for use
        self.preparing_data(data)
        self.efficiency.update(self.rune_data)
        # Rendering text
        self.render()
        # Creatinging Rect()
        self.creating_rect()

    def draw(self, surface):
        for key in self.render_data:
            surface.blit(self.render_data[key], self.rect_data[key])

        # Border Lines
        pygame.draw.rect(surface, "White", pygame.Rect((0, 0), DISPLAY_RUNE), 2, 1)
        # Side grid
        for key in IN_APP_GRID:
            pygame.draw.rect(surface, "White", IN_APP_GRID[key], 2, 1)

        for key, value in self.efficiency.grades.items():
            if value:
                pygame.draw.rect(
                    surface,
                    RUNE_QUALITY_BG_COLORS[value],
                    IN_APP_GRID[key],
                )
                surface.blit(
                    DEFAULT_RUNE_QUALITY[value],
                    DEFAULT_RUNE_QUALITY[value].get_rect(
                        center=IN_APP_GRID[key].center
                    ),
                )
            # Top grid
            pygame.draw.rect(surface, "White", IN_APP_GRID[key], 2)

        pygame.draw.rect(surface, "White", IN_APP_GRID["grinds"], 2, 1)
        pygame.draw.rect(surface, "White", IN_APP_GRID["roll_eff"], 2, 1)
