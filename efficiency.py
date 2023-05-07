import pygame
from math import ceil


class Efficiency:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 30, True)
        # List of information about rune
        self.rune_data = None
        # Rune roll efficiency [name,number%]
        self.ref = []
        # Information about rune grade
        self.grades = {}

        self.text_color = {
            "magic": (223, 242, 135),
            "rare": (185, 254, 255),
            "hero": (255, 213, 244),
            "legend": (255, 178, 72),
        }
        self.bg_color = {
            "magic": (30, 63, 6),
            "rare": (7, 66, 74),
            "hero": (92, 19, 65),
            "legend": (115, 50, 20),
        }
        self.default_grade = {
            "magic": self.font.render("Magic", True, self.text_color["magic"]),
            "rare": self.font.render("Rare", True, self.text_color["rare"]),
            "hero": self.font.render("Hero", True, self.text_color["hero"]),
            "legend": self.font.render("Legend", True, self.text_color["legend"]),
        }
        self.default_values = {
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

    def rune_eff(self):
        total = 0
        if self.ref:
            for value in self.ref:
                total += value[1]

            total = total / len(self.ref)
            # self.rune_efficiency = f"R.EFFICIENCY  {str(round(total))}%"
        # else:
        #     self.rune_efficiency = "NONE"

    def roll_efficiency(self, data):
        output = []
        try:
            for el_1, el_2 in data:
                el_1, el_2 = el_1.strip().lower(), el_2.strip()
                el_2 = int(el_2.replace("%", "").replace("+", ""))
                f = 0
                if el_1 in self.default_values:
                    # Calculates efficiency value
                    f = ((el_2 / self.default_values[el_1][1]) * 100) - 100
                    # checks if value negative
                    if f < 0:
                        f = 0
                output.append([el_1, round(f)])
            return output
        except ValueError:
            return []

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
        try:
            # Modifying data for use
            rune_data = [
                [y, int(x.replace("%", "").replace("+", ""))]
                for y, x in self.rune_data["subs"]
            ]

            for name, value in rune_data:
                try:
                    # Calculating roll number
                    roll_num = ceil(value / self.default_values[name.lower()][1])
                    # Modifying to get efficieny of lowest values
                    new_data.append(
                        [
                            name,
                            "+"
                            + str(roll_num * self.default_values[name.lower()][0])
                            + "%",
                        ]
                    )

                    total_rolls += roll_num
                except KeyError:
                    pass

            # Highest estimated possible Grade
            highest_grade = check_grade(total_rolls * 100)
            # Lowest estimated possible Grade

            f = self.roll_efficiency(new_data)
            total_rolls = sum([a[-1] for a in f])
            lowest_grade = check_grade(total_rolls)

            self.grades["el_grade"] = lowest_grade
            self.grades["eh_grade"] = highest_grade
        except IndexError or ValueError:
            self.grades["el_grade"] = None
            self.grades["eh_grade"] = None

        # Adds all efficiency of substats
        sub_total = sum([x[-1] for x in self.ref])
        # Checks the sub grade
        self.grades["sub_grade"] = check_grade(sub_total)

    def update(self, data):
        if data:
            self.rune_data = data
            # Checking sub efficiency
            self.ref = self.roll_efficiency(self.rune_data["subs"])
            # Checking rune efficiency
            self.rune_eff()
            # Checking grade
            self.rune_grade()
