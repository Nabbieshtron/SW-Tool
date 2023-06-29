import constants
from math import ceil


class Efficiency:
    def __init__(self):
        # User modified
        self.sub_stat_multipliers = {}
        self.synergy_multiplier = 0
        self.basic_value = True
        # List of information about rune
        self.rune_data = None
        # Rune roll efficiency str,int
        self.ref = {}
        # Rune efficiency
        self.rune_eff = "N"
        # Information about rune grade
        self.grades = {}

        # Default value of efficiency multiplier
        self.sub_modifiers: dict = {
            "no_flat": {
                "cri rate": 1,
                "cri dmg": 1,
                "atk": 1,
                "hp": 1,
                "def": 1,
                "resistance": 1,
                "accuracy": 1,
            },
            "flat": {
                "spd": 0.5,
                "atk": 0.5,
                "def": 0.5,
                "hp": 0.5,
            },
        }

    def rune_efficiency(self):
        ratio = 0.0
        state = "flat"

        # Main
        if len(self.rune_data["main"]) == 2:
            name, value = self.rune_data["main"]
            name = name.lower().strip()
            value, state = (
                (value[1:-1], "no_flat") if "%" in value else (value[1:], "flat")
            )

            if value.isdigit() and name in constants.DEFAULT_MAIN_POWER_UP[state]:
                level = int(self.rune_data["level"][0])

                # Formula: level * increment value + basic value == current value
                basic, increment, highest = constants.DEFAULT_MAIN_POWER_UP[state][name]

                if level == 15:
                    percent = lambda part, whole: int(whole / 100 * part + whole)

                    level -= 1
                    six_star = percent(20, level * increment[1] + basic[1])
                    five_star = percent(20, level * increment[0] + basic[1])
                else:
                    six_star = level * increment[1] + basic[1]
                    five_star = level * increment[0] + basic[0]

                # If True: 6 star grade
                if six_star == int(value):
                    ratio += 1.0

                # If True: 5 star grade
                elif five_star == int(value):
                    ratio += highest[0] / highest[1]
                else:
                    print("Check rune efficincy method")

                # Sub stat , inates
                for name, value, grinds in self.rune_data["subs"]:
                    name = name.lower().strip()
                    value, state = (
                        (value[1:-1], "no_flat")
                        if "%" in value
                        else (value[1:], "flat")
                    )
                    roll_values = constants.DEFAULT_SUB_VALUES[state]
                    if value.isdigit() and name in roll_values:
                        ratio += (
                            int(value)
                            / roll_values[name][1]
                            * 0.2
                            * self.sub_modifiers[state][name]
                        )
                    else:
                        self.rune_eff = "N"
                        break
                # Calculate efficiency
                total_eff = (ratio / 2.8) * 100
                self.rune_eff = str(ceil(total_eff))
            else:
                self.rune_eff = "N"
        else:
            self.rune_eff = "N"

    def roll_efficiency(self, data):
        output = {}
        try:
            for sub_name, sub_value in data:
                sub_name, sub_value = sub_name.strip().lower(), sub_value.strip()
                sub_value, state = (
                    (int(sub_value[1:-1]), "no_flat")
                    if "%" in sub_value
                    else (int(sub_value[1:]), "flat")
                )

                value = 0
                if sub_name in constants.DEFAULT_SUB_VALUES[state]:
                    # Calculates efficiency value
                    value = (
                        sub_value / constants.DEFAULT_SUB_VALUES[state][sub_name][1]
                    ) * 100
                    if self.basic_value is False:
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
        # 0 - len(rune_data) to remove 4 base values of substat
        total_rolls = 0 if self.basic_value else 0 - len(self.rune_data["subs"])
        highest_grade = None
        lowest_grade = None
        flag = True

        for sub_name, sub_value, grind_value in self.rune_data["subs"]:
            sub_name = sub_name.lower().strip()
            sub_value, state = (
                (sub_value[1:-1], "no_flat")
                if "%" in sub_value
                else (sub_value[1:], "flat")
            )
            if sub_value.isdigit():
                sub_value = int(sub_value)
                if sub_name in constants.DEFAULT_SUB_VALUES[state]:
                    lowest_roll, highest_roll = constants.DEFAULT_SUB_VALUES[state][
                        sub_name
                    ]
                    # Calculating roll number
                    roll_num = ceil(sub_value / highest_roll)

                    # New list for lowest quality
                    new_data.append([sub_name, f"+{str(roll_num * lowest_roll)}%"])
                    total_rolls += roll_num
                else:
                    flag = False
                    break
            else:
                flag = False
        if flag:
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
        else:
            self.grades["el_grade"] = ""
            self.grades["eh_grade"] = ""
            self.grades["sub_grade"] = ""

    def update(self, data):
        if data:
            self.rune_data = data
            # Checking sub efficiency
            self.ref = self.roll_efficiency([x[:-1] for x in self.rune_data["subs"]])
            # Checking rune efficiency
            self.rune_efficiency()
            # Checking grade
            self.rune_grade()
