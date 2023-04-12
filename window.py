import math
import pygame
from win32gui import GetClientRect, GetWindowRect


def get_size():
    hwnd = pygame.display.get_wm_info()["window"]
    rect = pygame.Rect(GetWindowRect(hwnd))
    client_rect = pygame.Rect(GetClientRect(hwnd))

    windowOffset = math.floor(((rect.w - rect.left) - client_rect.w) / 2)
    titleOffset = ((rect.h - rect.top) - client_rect.h) - windowOffset
    return (
        rect.left + windowOffset,
        rect.top + titleOffset,
        rect.w - windowOffset,
        rect.h - windowOffset,
    )
