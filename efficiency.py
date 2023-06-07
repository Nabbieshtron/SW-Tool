import pygame
from math import ceil


class Efficiency:
    def __init__(self):
        self.FONT = pygame.font.SysFont("Arial", 30, True)
        # User modified
        self.sub_stat_multipliers = {}
        self.synergy_multiplier = 0
        self.roll_efficiency_default_value = True
        self.rune_efficiency_inate = True
        # List of information about rune
        self.rune_data = None
        # Rune roll efficiency str,int
        self.ref = {}
        # Rune efficiency
        self.rune_eff = "N"
        # Information about rune grade
        self.grades = {}
        # Multiplier
        self.DEFAULT_EFFICIENCY_MULTIPLIER = 1

        self.TEXT_COLORS = {
            "magic": (223, 242, 135),
            "rare": (185, 254, 255),
            "hero": (255, 213, 244),
            "legend": (255, 178, 72),
        }
        self.BG_COLORS = {
            "magic": (30, 63, 6),
            "rare": (7, 66, 74),
            "hero": (92, 19, 65),
            "legend": (115, 50, 20),
        }

        self.DEFAULT_GRADES = {
            "magic": self.FONT.render("Magic", True, self.TEXT_COLORS["magic"]),
            "rare": self.FONT.render("Rare", True, self.TEXT_COLORS["rare"]),
            "hero": self.FONT.render("Hero", True, self.TEXT_COLORS["hero"]),
            "legend": self.FONT.render("Legend", True, self.TEXT_COLORS["legend"]),
        }
        self.SUB_DEFAULT_VALUES = {
            "cri rate": [4, 6],
            "spd": [4, 6],
            "cri dmg": [4, 7],
            "atk": [5, 8],
            "hp": [5, 8],
            "def": [5, 8],
            "resistance": [4, 8],
            "accuracy": [4, 8],
            "f_atk": [10, 20],
            "f_def": [10, 20],
            "f_hp": [135, 375],
        }

    def rune_efficiency(self):
        if self.ref:
            # Get synergy
            if list(self.ref.values()).count(max(self.ref.values())) > 1:
                print("duplicate")
            else:
                print("not dupe")
                print(self.rune_data["set"])

            # Calculate multipliers
            multiplier = 1.4
            # Get total value of roll efficiency
            total = sum(self.ref.values())
            # Calculate efficiency
            total_eff = total / 9 * multiplier
            self.rune_eff = str(ceil(total_eff))
        else:
            self.rune_eff = "N"

    def roll_efficiency(self, data):
        output = {}
        try:
            for sub_name, sub_value in data:
                sub_name, sub_value = sub_name.strip().lower(), sub_value.strip()
                if not all(x in sub_value for x in ("+", "%")) and sub_name != "spd":
                    sub_name = f"f_{sub_name}"

                sub_value = int(sub_value.replace("%", "").replace("+", ""))
                value = 0
                if sub_name in self.SUB_DEFAULT_VALUES:
                    # Calculates efficiency value
                    value = (sub_value / self.SUB_DEFAULT_VALUES[sub_name][1]) * 100
                    if self.roll_efficiency_default_value is False:
                        value -= 100

                    # checks if value negative
                    if value < 0:
                        value = 0
                output[sub_name] = value
            return output
        except ValueError:
            return {}

    def rune_grade(self):
        def check_grade(value):
            if value > 300:
                return "legend"
            elif value > 200:
                return "hero"
            elif value > 100:
                return "rare"
            elif value > 0:
                return "magic"
            else:
                return None

        # To calculate new efficiency
        new_data = []
        # 0 - len(rune_data) to remove 4 base substats
        total_rolls = 0 - len(self.rune_data["subs"])
        highest_grade = None
        lowest_grade = None

        for sub_name, sub_value, grind_value in self.rune_data["subs"]:
            sub_name = sub_name.lower().strip()
            name = sub_name
            if not all(x in sub_value for x in ("+", "%")) and name != "spd":
                name = f"f_{name}"

            try:
                sub_value = int(sub_value.replace("%", "").replace("+", ""))
            except ValueError:
                sub_value = 1
                # Calculating roll number
            try:
                roll_num = ceil(sub_value / self.SUB_DEFAULT_VALUES[name][1])
            except KeyError:
                roll_num = 1
            # Modifying to get efficieny of lowest values

            try:
                v = [sub_name, f"+{str(roll_num * self.SUB_DEFAULT_VALUES[name][0])}%"]
                if name in ("spd", "f_atk", "f_hp", "f_def"):
                    v[1] = v[1].replace("%", "")
                new_data.append(v)
            except KeyError:
                pass
            total_rolls += roll_num

        # Highest estimated possible Grade
        highest_grade = check_grade(total_rolls * 100)
        # Lowest estimated possible Grade
        total_rolls = sum(self.roll_efficiency(new_data).values())
        lowest_grade = check_grade(total_rolls)

        self.grades["el_grade"] = lowest_grade
        self.grades["eh_grade"] = highest_grade

        # Adds all efficiency of substats
        total = sum(self.ref.values())
        # Checks the sub grade
        self.grades["sub_grade"] = check_grade(total)

    def update(self, data):
        if data:
            self.rune_data = data
            # Checking sub efficiency
            self.ref = self.roll_efficiency([x[:-1] for x in self.rune_data["subs"]])
            # Checking rune efficiency
            self.rune_efficiency()
            # Checking grade
            self.rune_grade()
