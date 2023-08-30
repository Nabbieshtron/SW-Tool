from constants import DEFAULT_MAIN_POWER_UP, DEFAULT_SUB_VALUES


class Efficiency:
    def __init__(self):
        # User modified
        self.sub_stat_multipliers = {}
        self.synergy_multiplier = 0
        self.default_value:bool = False
        
        # Rune roll efficiency
        self.rune_roll_efficiency:list[int] = []
        
        # Rune efficiency
        self.rune_eff:str = ""
        
        # Grades
        self.grades:dict = {}
        
        
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
    
    # Calculating rune efficiency 
    def get_rune_efficiency(self, main_value, level, sub_values, innate=None):
        ratio:float = 0.0
        state:str = "flat"
        percent:int = lambda part, whole: int(whole / 100 * part + whole)

        # Adding main value ratio
        if all(main_value) and level[0]:
            name, value, state = main_value
            name, value = name.lower(), int(value)
            power_up_values = DEFAULT_MAIN_POWER_UP[state]
            
            if name in power_up_values:
                basic, increment, highest = power_up_values[name]
                level = int(level[0])

                # Calculating max rune main value
                if level == 15:
                    level -= 1
                    six_star = percent(20, level * increment[1] + basic[1])
                    five_star = percent(20, level * increment[0] + basic[0])
                else:
                    six_star = level * increment[1] + basic[1]
                    five_star = level * increment[0] + basic[0]

                # Checking if rune 6 star
                if six_star == value:
                    ratio += 1.0
                # Checking if rune 5 star
                elif five_star == value:
                    ratio += highest[0] / highest[1]
                else:
                    print("Efficiency Error")
            else:
                ratio = 0
        else:
            ratio = 0
        
        # Sub stat , inates
        if ratio > 0:
            for sub_name, sub_value, _, state in sub_values:
                sub_name, sub_value = sub_name.lower(), int(sub_value)
                roll_values = DEFAULT_SUB_VALUES[state]
                
                if sub_name in roll_values:
                    ratio += (
                        sub_value
                        / roll_values[sub_name][1]
                        * 0.2
                        * self.sub_modifiers[state][sub_name]
                    )
                else:
                    ratio = 0
                    break

        # Calculate efficiency
        self.rune_eff = str(round((ratio / 2.8) * 100)) if ratio > 0 else '0'

    def get_roll_efficiency(self, sub_values, innate=None):
        output = []
        if sub_values:
            for sub_name, sub_value, _, state in sub_values:
                sub_name, sub_value = sub_name.lower(), int(sub_value) 
                if sub_name in DEFAULT_SUB_VALUES[state]:
                    # Calculating roll efficiency value
                    value = (
                        sub_value / DEFAULT_SUB_VALUES[state][sub_name][1]
                    ) * 100

                    # Removing the defualt value
                    if self.default_value is False:
                        value -= 100

                    # if negative value = 0, else rounding the value
                    value = 0 if value < 0 else round(value)
                        
                    output.append(value)
            self.rune_roll_efficiency = output 
        else:
            self.rune_roll_efficiency = output 

    def get_grades(self, default_grade):
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
                return ""
        
        # Only if max amount of substatus values
        if len(self.rune_roll_efficiency) == 4:
            num = 500
            
            # Getting the largest number from substatus efficiency values
            max_stat = sum(self.rune_roll_efficiency)
            self.grades['sub_grade'] = check_grade(max_stat)
            
            # Reversing the substatus efficiency values allows us to check at which place the roll hit
            for value in reversed(self.rune_roll_efficiency):
                if value > 0:
                    num -= 100
                    break
                else:
                    num -= 100
            
            # Rune default grade
            self.grades['rune_grade'] = default_grade[0].lower() if default_grade else ""
        else:
            self.grades['rune_grade'] = ""
            self.grades['sub_grade'] = ""
        
    def update(self, data):
        if data:
            # Checking sub_status roll efficiency
            self.get_roll_efficiency(data["sub_values"])

            # Checking rune efficiency
            self.get_rune_efficiency(data['main_value'], data['level'], data['sub_values'])

            # Checking grade
            self.get_grades(data['default_grade'])
