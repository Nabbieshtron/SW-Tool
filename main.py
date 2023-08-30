import ctypes
import sys
from pathlib import Path

import pygame
from pytesseract import pytesseract

from app_handler import AppHandler
from display import Display_handler
from event_handler import Event_handler

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


class Main:
    def __init__(self):
        pygame.init()
        path_to_tesseract = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        pytesseract.tesseract_cmd = str(path_to_tesseract)
        pygame.display.set_caption("Sw Tool")
        self.clock = pygame.time.Clock()
        self.app_handler = AppHandler()
        self.display = Display_handler(self.app_handler)
        self.event_handler = Event_handler(self.app_handler, self.display)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.event_handler.video_resize()
                if event.type == pygame.KEYDOWN:
                    self.event_handler.key_down(event.key)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.event_handler.mouse_button_up(event.button)

            self.app_handler.update()
            self.display.update()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()
