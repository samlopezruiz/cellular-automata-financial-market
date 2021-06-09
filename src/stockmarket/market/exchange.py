from src.stockmarket.trader.agent import Trader
from numpy.random import choice, rand
from math import sqrt


class MarketExchange:

    def __init__(self, cfg, in_cfg):
        self.pb_rest = cfg['pb_rest']
        self.ttypes_dist = cfg['ttypes_dist']
        self.close_pb = cfg['close_pb']
        self.r_max = cfg['r_max']
        self.m = int(sqrt(cfg['n']))
        self.n = self.m ** 2
        self.traders = []
        self.wealth = cfg['wealth']
        self.stop_max = cfg['r_max'] + 0.01
        self.omega_max = cfg['omega_max']
        self.create_traders(in_cfg['watch'], in_cfg['debug'])
        self.d_t = 0

    def create_traders(self, watch, debug):
        ttypes = choice(['DEI', 'STP'], self.m ** 2, p=self.ttypes_dist)
        for c, ttype in enumerate(ttypes):
            if c in watch and debug:
                self.traders.append(Trader(ttype, self.omega_max, self.r_max,
                                           self.wealth, self.stop_max, self.pb_rest, self.close_pb, debug=True))
            else:
                self.traders.append(Trader(ttype, self.omega_max, self.r_max,
                                           self.wealth, self.stop_max, self.pb_rest, self.close_pb))

    def update_traders_values(self, r_max, stop_max):
        for trader in self.traders:
            trader.update_values(r_max, stop_max)

    def update_traders(self, p_t, sentiment):
        for trader in self.traders:
            trader.update(p_t, sentiment)

    def count_diff(self):
        diff = 0
        buyers, sellers = 0, 0
        for trader in self.traders:
            if trader.status == 1:
                buyers += 1
            if trader.status == -1:
                sellers += 1
            diff += trader.status

        self.d_t = diff / self.n
        return self.d_t


