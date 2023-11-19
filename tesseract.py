from cv2 import resize
from threading import Thread
from pytesseract import pytesseract

from collections import Counter
from pathlib import Path

        
class Tesseract:
    def __init__(self):
        # Preparing tesseract
        path_to_tesseract = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        pytesseract.tesseract_cmd = str(path_to_tesseract)\

        self.data_thread = None
        self.text_thread = None
        self.data:dict = {}
        self.text:dict = {'title': '', 'main': '', 'innate': '', 'substats': '', 'grade': ''}
        
    # Get verbose data including boxes, confidences, line and page numbers
    def get_multiple_data(self, images:dict):
        output = {}
        for key, image in images.items():
            output[key] = pytesseract.image_to_data(image, output_type='data.frame')
        self.data = output
        
    # Extracting text from images    
    def get_multiple_string(self, images:dict):
        output = {}
        for key, image in images.items():
          output[key] = pytesseract.image_to_string(image)
          
        # Updating dictionary
        self.text.update(output)
        self.data_thread, self.text_thread = None, None
          
    def update(self, images):
        if self.data_thread is None and self.text_thread is None:
            self.data_thread = Thread(target=self.get_multiple_data, args=(images,))
            self.text_thread = Thread(target=self.get_multiple_string, args=(images,))
            self.data_thread.start()
            
        elif not self.data_thread.is_alive() and not self.text_thread.is_alive():
            # Scaling image by the font size
            for key, data in self.data.items():
                # All the detected heights, iloc is a way to get data by the index
                heights = [int(x) for x in data.loc[:, 'height'] if isinstance(x, (int, float))]
                
                # Most commonly used height
                text_height = Counter(heights).most_common(1)[0][0]
                
                # Scale image to get correct font size
                height, width = images[key].shape[0], images[key].shape[1]
                scale_factor = 30 / text_height
                new_width = int(round(width * scale_factor))
                new_height = int(round(height * scale_factor))
                images[key] = resize(images[key], (new_width, new_height))
            self.text_thread.start()

