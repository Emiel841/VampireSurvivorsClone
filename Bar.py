import pygame


class Bar():
    def __init__(self, x, y, w, h, max, start, color, bgcolor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max = max
        self.value = start
        self.color = color
        self.bgcolor = bgcolor

    def draw(self, screen):
        ratio = self.value / self.max
        pygame.draw.rect(screen, self.bgcolor, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w *ratio, self.h))