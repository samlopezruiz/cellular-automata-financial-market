import time
from math import tanh, exp
import numpy as np
from src.stockmarket.board.cell import Patch
import pygame, sys
from pygame.locals import *
from src.stockmarket.board.cursor import cursor
import matplotlib.pyplot as plt


class ExchangeFloor:

    def __init__(self, market_exchange, cfg, in_cfg, patch_size=10):
        self.watch = {}
        self.mask = {}
        self.floor = {}
        self.patch_size = patch_size
        self.market_exchange = market_exchange
        self.m = market_exchange.m
        self.p = cfg['p']
        self.i_shock = cfg['I_shock']
        self.sentiment = 0
        self.res = self.m * self.patch_size
        self.resolution = [self.res, self.res]
        self.debug = in_cfg['debug']
        self.display = None
        self.animate = in_cfg['animate']
        self.impact = cfg['impact']
        self.get_mask()
        self.create_board()
        self.set_neighbours()
        self.ini_pygame()
        self.price_hist = []
        self.i_hist = []
        self.d_hist = []
        self.d_t = 0

    def ini_pygame(self):
        if not self.debug and self.animate:
            pygame.init()
            self.display = pygame.display.set_mode(self.resolution)
            pygame.display.set_caption('Market Exchange')

    def create_board(self):
        i = 0
        for x in range(0, self.m):
            for y in range(0, self.m):
                self.floor[x, y] = Patch(x, y, self.patch_size,
                                         self.market_exchange.traders[i])
                i += 1

    def set_neighbours(self):
        for x in range(0, self.m):
            for y in range(0, self.m):
                kx, ky = self.update_mask(x, y)
                neighbours = [self.floor[xi, yi].trader for xi, yi in zip(kx, ky)]
                self.floor[x, y].trader.set_neighbours(neighbours)

    def draw_board(self):
        for x in range(0, self.m):
            for y in range(0, self.m):
                self.floor[x, y].draw(self.display)

    def draw_grid(self):
        for x in range(0, self.m):
            for y in range(0, self.m):
                pygame.draw.line(self.display, (230, 230, 230), (x * self.patch_size, 0),
                                 (x * self.patch_size, self.m * self.patch_size))
                pygame.draw.line(self.display, (230, 230, 230), (0, y * self.patch_size),
                                 (self.m * self.patch_size, y * self.patch_size))

    def run_sime(self, n_iter=None, watch=[]):
        self.new_watch(watch)
        c = 0
        while True:
            if n_iter is not None:
                c += 1
                if not self.debug:
                    print("{}: p: {}, dt:{}".format(c, round(self.p, 4), round(self.d_t, 4)), end="\r")
                if c > n_iter:
                    if not self.debug and self.animate:
                        pygame.quit()
                    break

            self.market_step()
            self.append_watch(watch)

            if not self.debug and self.animate:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                self.draw_board()
                self.draw_grid()
                pygame.display.update()

    def append_watch(self, watch):
        for c, ix in enumerate(watch):
            td_t = self.market_exchange.traders[ix]
            self.watch[c]['status'].append(td_t.status)
            self.watch[c]['wealth'].append(td_t.wealth)
            self.watch[c]['omega_t'].append(td_t.omega_t)
            self.watch[c]['exp_r'].append(td_t.exp_r)
            self.watch[c]['stop_lim'].append(td_t.stop_lim)
            self.watch[c]['lambd'].append(td_t.lambd)
            self.watch[c]['b_t'].append(td_t.b_t)
            self.watch[c]['s_t'].append(td_t.s_t)
            self.watch[c]['pb_buy_t'].append(td_t.pb_buy_t)
            self.watch[c]['pb_sell_t'].append(td_t.pb_sell_t)
            self.watch[c]['p_buy'].append(td_t.p_buy)
            self.watch[c]['p_sell'].append(td_t.p_sell)
            self.watch[c]['counter'].append(td_t.counter)
            self.watch[c]['ttype'].append(td_t.ttype)
            self.watch[c]['price'].append(self.p)
        if self.debug:
            c = list(self.watch.keys())[0]
            print('p:{}, s:{}, c:{}, w:{}, t:{}, pb_b:{}, pb_s:{}, p_b:{}, p_s:{}, r:{}, l:{}, d:{}'.format(
                round(self.watch[c]['price'][-1], 2),
                self.watch[c]['status'][-1],
                self.watch[c]['counter'][-1],
                round(self.watch[c]['wealth'][-1], 2),
                self.watch[c]['ttype'][-1],
                round(self.watch[c]['pb_buy_t'][-1], 2),
                round(self.watch[c]['pb_sell_t'][-1], 2),
                round(self.watch[c]['p_buy'][-1], 2),
                round(self.watch[c]['p_sell'][-1], 2),
                round(self.watch[c]['exp_r'][-1], 2),
                round(self.watch[c]['stop_lim'][-1], 2),
                round(self.watch[c]['lambd'][-1], 2)
            ))

    def new_watch(self, watch):
        for c, _ in enumerate(watch):
            self.watch[c] = {}
            self.watch[c]['status'] = []
            self.watch[c]['wealth'] = []
            self.watch[c]['omega_t'] = []
            self.watch[c]['exp_r'] = []
            self.watch[c]['stop_lim'] = []
            self.watch[c]['lambd'] = []
            self.watch[c]['b_t'] = []
            self.watch[c]['s_t'] = []
            self.watch[c]['pb_buy_t'] = []
            self.watch[c]['pb_sell_t'] = []
            self.watch[c]['p_buy'] = []
            self.watch[c]['p_sell'] = []
            self.watch[c]['counter'] = []
            self.watch[c]['ttype'] = []
            self.watch[c]['price'] = []

    def get_mask(self):
        self.kernel_x = np.array([-1, -1, -1, 0, 0, 1, 1, 1]).flatten()
        self.kernel_y = np.array([-1, 0, 1, -1, 1, -1, 0, 1]).flatten()

    def update_mask(self, x, y):
        ky = self.kernel_y + y
        ky[ky == self.m] = 0
        ky[ky == -1] = self.m - 1

        kx = self.kernel_x + x
        kx[kx == self.m] = 0
        kx[kx == -1] = self.m - 1

        return kx, ky


    def new_coord(self, i, x):
        if i + x < 0:
            x0 = self.m - 1
        elif i + x >= self.m - 1:
            x0 = 0
        else:
            x0 = x + i
        return x0

    def update_neighbours(self):
        for trader in self.market_exchange.traders:
            trader.update_neighbours()

    def market_step(self):
        self.update_neighbours()
        self.market_exchange.update_traders(self.p, self.sentiment)
        self.d_t = self.market_exchange.count_diff()
        # market sentiment index
        self.sentiment = self.d_t + self.i_shock
        # price update
        self.p = self.p * (1 + tanh(self.impact * self.d_t))
        # self.p = (((exp(self.d_t) - exp(-self.d_t)) / (exp(self.d_t) + exp(-self.d_t)) + 1) * self.p - 1)

        self.append_to_history()

    def append_to_history(self):
        self.price_hist.append(self.p)
        self.i_hist.append(self.sentiment)
        self.d_hist.append(self.d_t)

    def get_map(self):
        X = np.zeros((self.m, self.m))
        for x in range(0, self.m):
            for y in range(0, self.m):
                X[x, y] = self.floor[x, y].trader.status
        return X
