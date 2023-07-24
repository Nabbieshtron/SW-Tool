from threading import Thread

from pytesseract import pytesseract

from artifact import Artifact
from constants import IN_APP_BG_COLOR
from image import Image
from rune import Rune


class Program:
    def __init__(self):
        self.initialize = True
        self.state = "rune"
        self.thread_state = False

        self.image = Image()
        self.rune = Rune()

        self.teseract_data = None

    def get_tesseract_data(self):
        self.thread_state = True
        # Converts image to text
        self.teseract_data: str = pytesseract.image_to_data(
            self.image.tese_img, output_type="dict"
        )["text"]
        self.thread_state = False

    def update(self):
        if self.initialize:
            for rect in self.image.rects.values():
                rect.modify_rect()
            self.initialize = False

        # Process image for use
        self.image.update()

        # Threading heavy task to resume even processes
        if not self.thread_state:
            Thread(target=self.get_tesseract_data).start()

        # Update rune data
        self.rune.update(self.teseract_data)

    def draw(self, surface):
        if self.state == "rune":
            surface.fill(IN_APP_BG_COLOR)
            self.rune.draw(surface)
