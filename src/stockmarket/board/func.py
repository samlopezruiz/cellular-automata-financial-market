import pygame
from src.stockmarket.board.cell import Patch
from src.stockmarket.trader.agent import Trader


def grid(surf):
    for x in range(0, 400 // 5):
        for y in range(0, (400 // 5)):
            pygame.draw.line(surf, (230, 230, 230), (x * 5, 0), (x * 5, 400))
            pygame.draw.line(surf, (230, 230, 230), (0, y * 5), (400, y * 5))


def create_board(board):  # creates my cells
    x = 0
    y = 0
    for x in range(0, 400 // 5):
        for y in range(0, (400 // 5)):
            board[x, y] = Patch(x, y, 5, None)



