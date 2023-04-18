import re
from itertools import groupby

import pygame
import image


class Program:
    def __init__(self):
        self.initialize = True
        self.state = "rune"

        self.bg_color: tuple[int] = (37, 24, 15)
        self.font = pygame.font.SysFont("Ariel", 30)

        self.screen_rect = pygame.Rect(0, 0, 600, 600)
        self.rects = None
        self.window_rect = None
        self.old_text = None
        self.rendered_texts = None
        self.text_rects = None

    @staticmethod
    def check_match(new_text, old_text):
        return not new_text == old_text

    def render_text(self, text):
        return self.font.render(text, True, (182, 165, 112))

    @staticmethod
    def create_text_rect(text_surf, pos_x, pos_y):
        return text_surf.get_rect(topleft=(pos_x, pos_y))

    def create_multiple_text_rect(self, text_surf: list, position: list):
        return [
            self.create_text_rect(surf, *pos.topleft)
            for surf, pos in zip(text_surf, position)
        ]

    @staticmethod
    def rm_spec_char(text: str, spec_char: str):
        pattern = re.compile(rf"{spec_char}")
        result = pattern.sub("", text)
        return result

    def join_char(self, text):
        if self.state == "rune":
            return ["".join(v) for _, v in groupby(text, str.isalpha)]
        else:
            original_lst = text.splitlines()
            print("Original", original_lst)
            # Modify strings
            lst = []
            for txt in original_lst:
                if txt:
                    if "of SPD" in txt:
                        text = txt.replace("of SPD", "").replace("by", "of SPD")
                        lst.append(text)
                    elif "of ATK" in txt:
                        text = txt.replace("of ATK", "").replace("by", "of ATK")
                        lst.append(text)
                    elif "of HP" in txt:
                        text = txt.replace("of HP", "").replace("by", "of HP")
                        lst.append(text)
                    elif "of DEF" in txt:
                        text = txt.replace("of DEF", "").replace("by", "of DEF")
                        lst.append(text)
                    else:
                        lst.append(txt)

            print("Edited_1", lst)
            new_lst = []
            # Separeting string from digits and creating new list
            for txt in lst:
                strip = txt.strip()
                split = strip.split(" ")
                rest = " ".join(split[:-1])
                rest = rest.replace(".", "")
                number = split[-1]
                new_lst.append(rest)
                new_lst.append(number)
            print("Edited_2", new_lst)
            return new_lst

    def efficiency(self, data: list[str], total_efficiency=False):
        """Return a tuple with substat name and efficiecy value"""
        # Modifying list to make it easier to work with
        sub_eff = []
        # This dictionary to get the total of substat value by the default value
        sub_value = None
        if self.state == "rune":
            sub_value = {
                "sv_6": 0,
                "sv_7": 0,
                "sv_8": 0,
                "sv_20": 0,
                "sv_375": 0,
            }
        else:
            sub_value = {
                "sv_03": 0,
                "sv_4": 0,
                "sv_5": 0,
                "sv_6": 0,
                "sv_8": 0,
                "sv_12": 0,
                "sv_14": 0,
                "sv_40": 0,
            }

        for substat, value in list(zip(data[::2], data[1::2])):
            # value of max substat
            sub_default_value = 1

            if self.state == "rune":
                # Flag to detect if value contains %
                flag = False
                value = self.rm_spec_char(value, r"[^0-9%]")
                value = "".join(value)

                if "%" in value:
                    value = self.rm_spec_char(value, r"[^0-9]")
                    value = int("".join(value)) if value else 0
                    flag = True
                else:
                    flag = False
                    value = int("".join(value)) if value else 0

                if substat.lower() == "crirate" and flag is True:
                    sub_default_value = 6
                    sub_value["sv_6"] += value
                if substat.lower() == "spd" and flag is False:
                    sub_default_value = 6
                    sub_value["sv_6"] += value
                if substat.lower() == "cridmg" and flag is True:
                    sub_default_value = 7
                    sub_value["sv_7"] += value
                if (
                    substat.lower() in ("atk", "hp", "def", "resistance", "accuracy")
                    and flag is True
                ):
                    sub_default_value = 8
                    sub_value["sv_8"] += value
                if substat.lower() in ("atk", "def") and flag is False:
                    sub_default_value = 20
                    sub_value["sv_20"] += value
                if substat.lower() == "hp" and flag is False:
                    sub_default_value = 375
                    sub_value["sv_375"] += value

            elif self.state == "artifact":
                value = self.rm_spec_char(value, r"[^0-9%.]")
                if "-" in substat[:2]:
                    substat = substat.replace("-", "", 1).strip()
                else:
                    substat = substat.strip()
                if value and value != ".":
                    value = float(value) if "." in value else int(value)
                else:
                    value = 0

                if substat.lower() == "add'l dmg of hp":
                    sub_default_value = 0.30
                    sub_value["sv_03"] += value
                if substat.lower() in (
                    "own turn 1-target cd",
                    "def up effect",
                    "counterattack dmg",
                    "co-op attack dmg",
                    "bomb dmg",
                    "add'l dmg of atk",
                    "add'l dmg of def",
                    "crit dmg taken",
                ):
                    sub_default_value = 4
                    sub_value["sv_4"] += value
                if substat.lower() in (
                    [
                        f"dmg dealt on {x}"
                        for x in ["fire", "water", "wind", "light", "dark"]
                    ]
                    + ["atk up effect"]
                ):
                    sub_default_value = 5
                    sub_value["sv_5"]
                if substat.lower() in (
                    [f"[s{x}] crit dmg" for x in range(1, 5)]
                    + [f"[s{x}] recovery" for x in range(1, 4)]
                    + [f"[s{x}] accuracy" for x in range(1, 4)]
                    + [
                        f"dmg taken from {x}"
                        for x in ["fire", "water", "wind", "light", "dark"]
                    ]
                    + [
                        "cd as more enemy hp, max",
                        "spd up effect",
                        "hp when revived",
                        "atk bar when revived",
                    ]
                ):
                    sub_default_value = 6
                    sub_value["sv_6"] += value
                if substat.lower() == "life drain":
                    sub_default_value = 8
                    sub_value["sv_8"]
                if substat.lower() == "cd as less enemy hp, max":
                    sub_default_value = 12
                    sub_value["sv_12"] += value
                if substat.lower() in [
                    f"{x} prop lost hp, max" for x in ("atk", "def", "spd")
                ]:
                    sub_default_value = 14
                    sub_value["sv_14"] += value
                if substat.lower() == "add'l dmg of spd":
                    sub_default_value = 40
                    sub_value["sv_40"] += value
            efficiency_roll = ((value / sub_default_value) * 100) - 100
            if efficiency_roll < 0:
                efficiency_roll = 0
            sub_eff.append((substat, str(round(efficiency_roll)), "%"))

        if total_efficiency and self.state == "rune":
            current_efficiency = 0
            for key, value in sub_value.items():
                if value > 0:
                    if key == "sv_6":
                        current_efficiency += value / 6
                    elif key == "sv_7":
                        current_efficiency += value / 7
                    elif key == "sv_8":
                        current_efficiency += value / 8
                    elif key == "sv_20":
                        current_efficiency += value / 20
                    elif key == "sv375":
                        current_efficiency += value / 375
            # In this place the 8 number should be different by the quality of rune
            # but it can stay 8 because it maximum sub roll 4 by default and if legendary rune 4 more rolls
            # would be 9 if innate included
            current_efficiency = (current_efficiency / 8) * 100
            sub_eff.append(("Efficiency", str(round(current_efficiency)), "%"))
        else:
            pass
        return sub_eff

    def update(self):
        if self.initialize:
            self.screen_rect = pygame.Rect(0, 0, *pygame.display.get_window_size())
            for rect in self.rects.values():
                rect.modify_rect()
            self.initialize = False

        # Get full_screenshot
        pil_image = image.get_image()
        # Crop the image from the screenshot

        croped_image = image.crop_image(
            pil_image,
            self.window_rect.left + 110,
            self.window_rect.top + 10,
            self.window_rect.w - 10,
            self.window_rect.h - 10,
        )
        # Get the list of cropped images (should be 4 images)
        images = image.crop_multiple_image(
            croped_image, [rect.rect for rect in self.rects.values()]
        )

        # Resize images for blit
        images = image.resize_multiple_images(
            images, [rect.default_rect.size for rect in self.rects.values()]
        )

        # Calculates the total width and height of images
        total_size = image.get_total_image_size(images[3:])

        # Creating new image and stiching together to minimize performance time
        new_img = image.new_image("RGB", total_size, self.bg_color)
        new_img = image.stich_multiple_image(new_img, images[3:])

        text_inate = ""
        # Get text from image
        if self.state == "rune":
            text_inate = image.get_image_text(images[2])
        text_sub = image.get_image_text(new_img)

        # Convert images to surface
        self.images_surf = image.convert_pils_to_surfaces(images)

        # Image surfaces rect
        if self.state == "rune":
            self.image_surf_rect = [
                r1 := self.images_surf[0].get_rect(
                    center=(self.screen_rect.width / 2, 60)
                ),
                self.images_surf[1].get_rect(
                    centerx=(self.screen_rect.width / 2), top=r1.bottom - 2
                ),
                r2 := self.images_surf[2].get_rect(center=(120, 200)),
                self.images_surf[3].get_rect(centerx=120, top=r2.bottom - 2),
            ]
        else:
            self.image_surf_rect = [
                r1 := self.images_surf[0].get_rect(
                    center=(self.screen_rect.width / 2, 60)
                ),
                self.images_surf[1].get_rect(
                    centerx=(self.screen_rect.width / 2), top=r1.bottom - 2
                ),
                self.images_surf[3].get_rect(topleft=(50, 200)),
            ]

        # Efficiency block rect
        self.efficiency_rect = [rect.copy() for rect in self.image_surf_rect[2:]]
        self.efficiency_rect.append(self.image_surf_rect[2].copy())
        self.efficiency_rect[-1].top = self.efficiency_rect[-2].bottom - 2

        # Position managment
        if self.state == "rune":
            for rect in self.efficiency_rect:
                rect.centerx = 480
        else:
            for rect in self.efficiency_rect:
                rect.w += 50
                rect.centerx = 660
            self.efficiency_rect[-1].h = 50

        # This if check helps to minimize performance time (should work without it)
        if self.check_match(text_sub, self.old_text):
            self.old_text = text_sub
            # Removes the symbols with some excluded and returns a list of strings -> letters
            if self.state == "rune":
                m_text_sub = self.rm_spec_char(text_sub, r"[^a-zA-Z0-9\+\%]")
            else:
                m_text_sub = self.rm_spec_char(text_sub, r"[^a-zA-Z0-9\]\[\'\,\.\n\- ]")
            print(m_text_sub)
            # Join the strings and returns the list of strings -> text
            sub_list = self.join_char(m_text_sub)
            print(sub_list)
            # Using equations returns the modified data as a list of strings -> text
            sub_list = self.efficiency(sub_list, True)
            # Joins the text into sentences
            sub_list = [" ".join(text) for text in sub_list]
            # In this list should be from 1 to 4 elements
            rendered_sub_list = [self.render_text(text) for text in sub_list]
            sub_rect = [text.get_rect() for text in rendered_sub_list]

            # Position managment
            n = 0
            try:
                if self.state == "rune":
                    for rect in sub_rect[:-1]:
                        rect.left = 390
                        rect.top = 230 + n
                        n += 30
                    sub_rect[-1].topleft = (390, 360)
                else:
                    for rect in sub_rect:
                        rect.left = 480
                        rect.top = 215 + n
                        n += 30
            except IndexError:
                pass

            sub_text_rect = self.create_multiple_text_rect(rendered_sub_list, sub_rect)
            inate_text_rect = []
            rendered_inate_list = []

            if text_inate and self.state == "rune":
                m_text_inate = self.rm_spec_char(text_inate, r"[^a-zA-Z0-9%]")
                inate_list = self.join_char(m_text_inate)
                inate_list = self.efficiency(inate_list)
                inate_list = [" ".join(text) for text in inate_list]
                # In this list should be only 1 or 0 elements
                rendered_inate_list = [self.render_text(text) for text in inate_list]
                inate_rect = [text.get_rect() for text in rendered_inate_list]

                for rect in inate_rect:
                    rect.left = 390
                    rect.top = 190
                try:
                    inate_text_rect = self.create_text_rect(
                        rendered_inate_list[0], *inate_rect[0].topleft
                    )
                except IndexError:
                    pass

            if rendered_inate_list and inate_text_rect and self.state == "rune":
                self.rendered_texts = [*rendered_sub_list, rendered_inate_list[0]]
                self.text_rects = [*sub_text_rect, inate_text_rect]
            else:
                self.rendered_texts = [*rendered_sub_list]
                self.text_rects = [*sub_text_rect]

    def draw(self, surface):
        surface.fill(self.bg_color)

        if self.state == "rune":
            for surf, rect in zip(self.images_surf, self.image_surf_rect):
                surface.blit(surf, rect)
                pygame.draw.rect(surface, (145, 119, 26), rect, 2)
            for text, rect in zip(self.rendered_texts, self.text_rects):
                surface.blit(text, rect)
            for rect in self.efficiency_rect:
                pygame.draw.rect(surface, (145, 119, 26), rect, 2)

        else:
            del self.images_surf[2]
            del self.efficiency_rect[-1]

            self.image_surf_rect[-1].top += 5
            surface.blit(self.images_surf[-1], self.image_surf_rect[-1])
            self.image_surf_rect[-1].top -= 5
            pygame.draw.rect(surface, (145, 119, 26), self.image_surf_rect[-1], 2)

            for surf, rect in zip(self.images_surf[:-1], self.image_surf_rect[:-1]):
                surface.blit(surf, rect)
                pygame.draw.rect(surface, (145, 119, 26), rect, 2)

            for text, rect in zip(self.rendered_texts, self.text_rects):
                surface.blit(text, rect)

            for rect in self.efficiency_rect:
                pygame.draw.rect(surface, (145, 119, 26), rect, 2)
