from threading import Thread

from pytesseract import pytesseract

from artifact import Artifact
from constants import IN_APP_BG_COLOR
from image import Image
from rune import Rune
from collections import Counter

class Program:
    def __init__(self):
        self.initialize = True
        self.state = "rune"
        self.thread_state = False

        self.image = Image()
        self.rune = Rune()

        self.teseract_data = {}

    def most_common_number(self, numbers):
        return Counter(numbers).most_common(1)[0][0]
        
    def get_tesseract_data(self, image, key):
        self.thread_state = True
        
        # Get verbose data including boxes, confidences, line and page numbers
        data = pytesseract.image_to_data(image, output_type='data.frame')
        rows = []
        
        # All the detected heights, iloc is a way to get data by the index
        heights = [int(x) for x in data.loc[:, 'height'] if isinstance(x, (int, float))]
        
        # Most commonly used height
        text_height = self.most_common_number(heights)
        
        # Scale image to get correct text size
        scaled_image = self.image.scale_image(image, text_height)
        
        # Extracting text from the prepared image
        self.teseract_data[key] = pytesseract.image_to_string(scaled_image)

        self.thread_state = False

    def update(self):
        if self.initialize:
            for rect in self.image.rects.values():
                rect.modify_rect()
            self.initialize = False

        # Process image for use
        self.image.update()

        # Threading heavy task to resume event processes
        if not self.thread_state:
            for img, key in zip(self.image.tese_imgs, ['title', 'main_value', 'innate', 'sub_values', 'default_grade']):
                Thread(target=self.get_tesseract_data(img, key)).start()

        # Update rune data
        self.rune.update(self.teseract_data)

    def draw(self, surface):
        if self.state == "rune":
            surface.fill(IN_APP_BG_COLOR)
            self.rune.draw(surface)
