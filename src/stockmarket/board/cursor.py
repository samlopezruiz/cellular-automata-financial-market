import pygame
black = (0, 0, 0)  # black

class cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 5
        self.h = 5
        self.col = black

    def drawcursor(self, surf):
        pygame.draw.rect(surf, self.col, (self.x * self.w, self.y * self.h, self.w, self.h), 1)
