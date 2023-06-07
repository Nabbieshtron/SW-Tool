import pygame
from pytesseract import pytesseract

from image import Image
from rune import Rune
from artifact import Artifact


class Program:
    def __init__(self):
        self.initialize = True
        self.state = "rune"
        self.match_state = False
        self.bg_color: tuple[int] = (37, 24, 15)
        self.screen_rect = pygame.Rect(0, 0, 600, 600)

        self.image = Image()
        self.rune = Rune()

        self.old_teseract_data = None
        self.teseract_data = None

    def check_match(self):
        self.match_state = (
            True
            if self.old_teseract_data is None
            else self.teseract_data != self.old_teseract_data
        )

    def update(self):
        if self.initialize:
            self.screen_rect = pygame.Rect(0, 0, *pygame.display.get_window_size())
            for rect in self.image.rects.values():
                rect.modify_rect()
            self.initialize = False

        # Process image for use
        self.image.update()

        # Converts image to text
        self.teseract_data: str = pytesseract.image_to_data(
            self.image.tese_img, output_type="dict"
        )["text"]

        # If check for old data is same as new data to save performance
        self.check_match()
        if self.match_state:
            # Update rune data
            self.rune.update(self.teseract_data)
            # Saving new data as old
            self.old_teseract_data = self.teseract_data

    def draw(self, surface):
        if self.state == "rune" and self.match_state:
            surface.fill(self.bg_color)
            self.rune.draw(surface)
