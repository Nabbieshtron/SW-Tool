import pygame
import math



class Rects:
    transparent_rect = pygame.Rect(110, 10, 480, 340)

    def __init__(self, position:tuple[int], size:tuple[int]):
        self.flag = True
        self.rect = pygame.Rect(position, size)
        self.rect_ratio = self.get_ratio_list()

    def get_ratio_list(self):
        return [
            (self.rect.x - self.transparent_rect.x) / self.transparent_rect.w,
            (self.rect.y - self.transparent_rect.y) / self.transparent_rect.h,
            self.rect.w / self.transparent_rect.w,
            self.rect.h / self.transparent_rect.h,
        ]

    def get_scaled_rect(self):
        self.rect = pygame.Rect(
            self.rect_ratio[0] * self.transparent_rect.w + self.transparent_rect.x,
            self.rect_ratio[1] * self.transparent_rect.h + self.transparent_rect.y,
            self.rect_ratio[2] * self.transparent_rect.w,
            self.rect_ratio[3] * self.transparent_rect.h,
        )

    def modify_rect(self):
        self.rect = pygame.Rect(
            self.rect.left - self.transparent_rect.left + 2,
            self.rect.top - self.transparent_rect.top + 2,
            self.rect.w + (self.rect.left - self.transparent_rect.left) - 2,
            self.rect.h + (self.rect.top - self.transparent_rect.top) - 2,
        )

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect, 2)



