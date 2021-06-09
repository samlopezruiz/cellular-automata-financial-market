import pygame
import sys
from pygame.locals import *
from src.stockmarket.board.cursor import cursor
from src.stockmarket.board.func import create_board, grid

if __name__ == '__main__':
    resolution = [400, 400]

    pygame.init()
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Board Sim')
    board = {}
    retCur = cursor(0, 0)
    create_board(board)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:  # My problem starts here
                mx, my = pygame.mouse.get_pos()
                mx = (mx / 5)
                my = (my / 5)
                print("Celula pos x %i, pos y %i" % (mx, my))
                retCur.x = mx
                retCur.y = my

        for x in range(0, (400 // 5)):
            for y in range(0, (400 // 5)):
                board[x, y].draw_rand(display)

        grid(display)
        retCur.drawcursor(display)
        pygame.display.update()