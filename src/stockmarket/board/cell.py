import pygame
from numpy.random import rand

red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
white = (220, 220, 220)
gray = (200, 200, 200)


class Patch:

    def __init__(self, x, y, patch_size, trader, buy_color=red,
                 sell_color=blue, board_color=black, operation_color=gray):
        self.x = x
        self.y = y
        self.w = patch_size
        self.h = patch_size
        self.trader = trader
        self.buy_color = buy_color
        self.sell_color = sell_color
        self.board_color = board_color
        self.operation_color = operation_color
        self.color = self.board_color

    def draw(self, surf):
        # if self.trader.p_buy > 0:
        #     self.color = self.buy_color
        # elif self.trader.p_sell > 0:
        #     self.color = self.sell_color
        if self.trader.status == 1:
            self.color = self.buy_color
        elif self.trader.status == -1:
            self.color = self.sell_color
        elif self.trader.p_buy > 0 or self.trader.p_sell > 0:
            self.color = self.operation_color
        else:
            self.color = self.board_color
        pygame.draw.rect(surf, self.color,
                         (self.x * self.w, self.y * self.h, self.w, self.h), 0)

    def draw_rand(self, surf):
        r = rand()
        if r < 0.25:
            self.color = self.buy_color
        elif 0.25 <= r < 0.5:
            self.color = self.sell_color
        else:
            self.color = self.board_color
        pygame.draw.rect(surf, self.color,
                         (self.x * self.w, self.y * self.h, self.w, self.h), 0)