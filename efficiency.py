from constants import DEFAULT_MAIN_POWER_UP, DEFAULT_SUB_VALUES


class Efficiency:
    def __init__(self):
        # User modified
        self.sub_stat_multipliers = {}
        self.synergy_multiplier = 0
        self.basic_value = False
        # List of information about rune
        self.rune_data = None
        # Rune roll efficiency str,int
        self.rolls = []
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
                "spd": 1,
                "atk": 0.5,
                "def": 0.5,
                "hp": 0.5,
            },
        }

    def rune_efficiency(self):
        ratio = 0.0
        state = "flat"
        percent = lambda part, whole: int(whole / 100 * part + whole)

        # Main
        if len(self.rune_data["main"]) == 2:
            name, value = self.rune_data["main"]
            name = name.lower().strip()
            value, state = (
                (value[1:-1], "no_flat") if "%" in value else (value[1:], "flat")
            )

            if value.isdigit() and name in DEFAULT_MAIN_POWER_UP[state]:
                level = int(self.rune_data["level"][0])
                basic, increment, highest = DEFAULT_MAIN_POWER_UP[state][name]

                # Getting main value
                if level == 15:
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
                    print("Efficiency Error")
        else:
            ratio = 0

        # Sub stat , inates
        if ratio > 0:
            for name, value, grinds in self.rune_data["subs"]:
                name = name.lower().strip()
                value, state = (
                    (value[1:-1], "no_flat") if "%" in value else (value[1:], "flat")
                )
                roll_values = DEFAULT_SUB_VALUES[state]
                if value.isdigit() and name in roll_values:
                    ratio += (
                        int(value)
                        / roll_values[name][1]
                        * 0.2
                        * self.sub_modifiers[state][name]
                    )
                    print(
                        (
                            int(value)
                            / roll_values[name][1]
                            * 0.2
                            * self.sub_modifiers[state][name]
                        )
                    )
                else:
                    ratio = 0
                    break

        # Calculate efficiency
        self.rune_eff = str(round((ratio / 2.8) * 100)) if ratio > 0 else ""

    def roll_efficiency(self, data):
        output = []
        try:
            for sub_name, sub_value in data:
                sub_name, sub_value = sub_name.strip().lower(), sub_value.strip()
                sub_value, state = (
                    (sub_value[1:-1], "no_flat")
                    if "%" in sub_value
                    else (sub_value[1:], "flat")
                )
                value = 0
                if sub_name in DEFAULT_SUB_VALUES[state]:
                    # Calculates efficiency value
                    value = (
                        int(sub_value) / DEFAULT_SUB_VALUES[state][sub_name][1]
                    ) * 100

                    # Basic Value check
                    if self.basic_value is False:
                        value -= 100

                    # checks if value negative
                    if value < 0:
                        value = 0

                output.append(value)
            return output
        except ValueError:
            return []

    def rune_grade(self):
        def check_grade(value):
            if value >= 300:
                return "legend"
            elif value >= 200:
                return "hero"
            elif value >= 100:
                return "rare"
            elif value >= 0:
                return "magic"
            else:
                return None

        # Checks the sub grade
        self.grades["sub_grade"] = check_grade(sum(self.rolls))

        if len(self.rolls) > 3:
            # Value of substat line on rune
            num = 500
            # Max value from all substats
            max_stat = max(self.rolls)

            sub_stats = self.rolls[1:] if len(self.rolls) == 5 else self.rolls
            for value in reversed(sub_stats):
                if value > 0:
                    num -= 100
                    break
                else:
                    num -= 100

            self.grades["rune_grade"] = check_grade(max(num, max_stat))

        else:
            self.grades["rune_grade"] = ""

    def update(self, data):
        if data:
            self.rune_data = data
            # Checking sub efficiency
            self.rolls = self.roll_efficiency([x[:-1] for x in self.rune_data["subs"]])
            # Checking rune efficiency
            self.rune_efficiency()
            # Checking grade
            self.rune_grade()
