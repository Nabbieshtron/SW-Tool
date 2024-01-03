import pygame
import cv2

class ImageManager:
    def __init__ (
        self, 
        window:pygame.Rect, 
        transparent:pygame.Rect,
        navigation_rects: tuple[pygame.Rect]
        ):
        self.window_rect = window
        self.transparent_rect = transparent
        self.navigation_rects = navigation_rects
    
    def update_navigation_boxes(self):
        # Calculating the new _rect position
        x = window_rect.x + _rect.x
        y = window_rect.y + _rect.y
        w = window_rect.w - transparent_rect.y - (transparent_rect.right - _rect.right)
        h = window_rect.h - transparent_rect.y - (transparent_rect.bottom - _rect.bottom)
    
    def update_navigation_boxes_images(self) -> dict:
        for key, _rect in navigation_rects.items():

            # Croping the image from main image
            cropped_img = image[y:h, x:w]
            
            # Invert image
            inverted_image = cv2.bitwise_not(cropped_img)

            # Gray scaled image
            gray_scaled_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)

            # Binaryse the image (make it black and white)
            threshold_value = 170
            max_value = 230
            if key == 'grade':
                threshold_value = 130
                max_value = 230
                
            thresh, image_bw = cv2.threshold(gray_scaled_image, threshold_value, 
                max_value, cv2.THRESH_BINARY)

            self.tese_images[key] = image_bw

    def processing_image(self, image):
    # for key, dims in self.persist['navigation_rect_attributes'].items():
        # navigation_rects[key] = pygame.Rect(*dims.values())
