from PIL import ImageGrab as PilIg
import cv2
import numpy as np


class Image:
    def __init__(self):
        self.window_rect = None
        self.rects = None
        # One image of data
        self.img = None
        # Multiple images of data
        self.imgs = None
        # Tesseract image for extraction
        self.tese_img = None

    def convert_from_image_to_cv2(self, image):
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
    def crop_image(self, x_pos, y_pos, width, height, image):
        return image[y_pos:height, x_pos:width]
        
    def scale_image(self, image, float_value):
        height, width = image.shape[0], image.shape[1]
        scale_factor = 30 / float_value
        new_width = int(round(width * scale_factor))
        new_height = int(round(height * scale_factor))
        return cv2.resize(image, (new_width, new_height))
        
    def update(self):
        # Crop position
        x, y, w, h =  self.window_rect.left + 110, self.window_rect.top + 10, self.window_rect.w - 10, self.window_rect.h - 10
        
        # Get full_screenshot
        img = PilIg.grab(all_screens=False)
        
        # Convert pil to cv2
        img = self.convert_from_image_to_cv2(img)
        
        # Main image
        img = self.crop_image(x, y, w, h, img)

        # Preprocesing the image
        images = []
        
        for rect in self.rects.values():
            # Crop position
            x, y, w, h = rect.rect
            
            # Croping the image from main image
            cropped_img = self.crop_image(x, y, w, h,img)
            
            # Invert image
            inverted_image = cv2.bitwise_not(cropped_img)
            
            # Gray scaled image
            gray_scaled_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
            
            # Binaryse the image (make it black and white)
            thresh, im_bw = cv2.threshold(gray_scaled_image, 170, 230, cv2.THRESH_BINARY)
            
            # Erode image
            eroded_image = (im_bw)

            images.append(eroded_image)

        self.tese_imgs = images
