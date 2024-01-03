import re
from cv2 import resize
from threading import Thread
import threading
from pytesseract import pytesseract

from collections import Counter
from pathlib import Path

from constants import RUNE_SETS

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
    
    def parse_data(self) -> dict:
        '''Parsing string data'''
        rune_data = {
            'title': None,
            'main': None,
            'set_': None,
            'slot': None,
            'level': None,
            'innate': None,
            'substats': None,
            'grade': None,
        }

        # Adding correct spacing between values
        for key in ('title','main','innate','substats','grade'):
            if type(self.text[key]) is str:
                value = self.text[key].replace('\n','').replace(' ', '')
                value = re.sub('([a-z])([A-Z])', r'\g<1> \g<2>', value)
                rune_data[key] = re.sub('([A-Z])([A-Z])([a-z])', r'\g<1> \g<2>\g<3>', value)
            if key not in ('substats', 'grade'):
                rune_data[key] = re.findall('[A-Za-z ]+|[^A-Za-z €()]+', rune_data[key])
                
        # Slot, level, title, set
        try:
            level, title, slot = rune_data.get('title')
            
            value = re.search('[1-6]', slot)
            if value is None:
                raise ValueError
            else:
                rune_data['slot'] = value.group()
            
            value = re.search('[0-9]+', level)
            if value is None:
                raise ValueError
            else:
                rune_data['level'] = int(value.group())

            rune_data['title'] = title
            
            set_ = [rune_set for rune_set in RUNE_SETS if rune_set in title.lower()]
            rune_data['set_'] = set_[0]

        except (ValueError, IndexError):
            rune_data['slot'] = ''
            rune_data['level'] = ''
            rune_data['set_'] = ''
            rune_data['title'] = 'Adjust the position'

        # Main
        try:
            if rune_data.get('title', '') == 'Adjust the position':
                raise ValueError
                
            name, value = rune_data.get('main')
            flat = True if "%" not in value else False
            value = re.search('[0-9]+', value)
            if value is None:
                raise ValueError
            else:
                value = value.group()
            rune_data['main'] = [name, int(value), flat]
        except ValueError:
            rune_data['main'] = ['', '', True]

        # Innate
        try:
            name, value = rune_data.get('innate')
            flat = True if "%" not in value else False
            value = re.search('[0-9]+', value)
            if value is None:
                raise ValueError
            else:
                value = value.group()
            rune_data['innate'] = [name, int(value), flat]
        except ValueError:
            rune_data['innate'] = ['', '', True]
            
        # Substats
        rx = re.compile(r'([a-ik-zA-IK-Z]+(?:\s+[a-zA-Z]+)?)\s*(\+\d+%?)\s*(\+\d+%?)?')
        substats = [list(t) for t in rx.findall(rune_data['substats'])]

        subs = []
        
        for sub_name, sub_value, grind in substats:
            flat = True if "%" not in sub_value else False
            
            # Removing noise
            sub_value = re.search('[0-9]+', sub_value).group()
            grind = re.search('[0-9]+', grind).group() if grind else ''
            
            subs.append([sub_name, int(sub_value), grind, flat])
        
        rune_data['substats'] = subs
        return rune_data
        
    def update(self, images):
        threading.active_count()
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

