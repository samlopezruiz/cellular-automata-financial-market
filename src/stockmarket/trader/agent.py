from numpy.random import rand


class Trader:

    def __init__(self, ttype, omega_max, r_max, wealth=100,
                 stop_max=0.02, pb_rest=0.1, close_pb=0.0, debug=False):
        self.pb_rest = pb_rest
        self.counter = 0
        self.ttype = ttype
        self.wealth = wealth
        self.omega_max = omega_max
        self.omega_t = rand() * self.omega_max
        self.r_max = r_max
        self.stop_max = stop_max
        self.transactions = 0
        self.debug = debug
        self.close_pb = close_pb
        # influenced by the sentiment [0,1)
        self.beta = rand()  # rand() * self.exp_r
        # trader expected return
        self.exp_r = rand() * self.r_max
        # Stop loss rule parameter
        self.stop_lim = rand() * self.stop_max
        # Prospect theory parameter
        self.lambd = 2.25 * self.exp_r
        # buyers around agent [0, 8]
        self.b_t = 0
        # sellers around agent [0, 8]
        self.s_t = 0
        # prob. agent will buy  [0, 1]
        self.pb_buy_t = 0
        # extra information advising him to buy [0, 1]
        self.O_buy_t = 0
        # prob. agent will sell  [0, 1]
        self.pb_sell_t = 0
        # extra information advising him to sell [0, 1]
        self.O_sell_t = 0
        # buyer or seller (1, -1)
        self.status = 0
        # price @ buy
        self.p_buy = 0
        # price @ sell
        self.p_sell = 0
        self.short_selling = False
        # sentiment
        self.I = 0
        self.neighbours = []

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def update_neighbours(self): #, b_t, s_t):
        buyers, sellers = 0, 0
        for neigh in self.neighbours:
            status = neigh.status
            if status == 1:
                buyers += 1
            elif status == -1:
                sellers += 1
        self.b_t = buyers
        self.s_t = sellers

    def update_values(self, r_max, stop_max):
        pass
        # self.r_max = r_max
        # self.stop_max = stop_max
        # self.exp_r = rand() * self.r_max
        # # Stop loss rule parameter
        # self.stop_lim = rand() * self.stop_max
        # # Prospect theory parameter
        # self.lambd = 2.25 * self.exp_r

    def update(self, p_t, sentiment):
        self.I = sentiment
        if self.ttype == 'DEI':
            self.disp_effect(p_t)
        else:
            self.stop_loss(p_t)

    def update_prob(self):
        self.omega_t = rand() * self.omega_max
        # self.pb_buy_t = (self.b_t + self.omega_t * self.O_buy_t) / (8 + self.omega_t * self.O_buy_t) + \
        #                (self.beta * self.I if self.I > 0 else 0)
        # self.pb_sell_t = (self.s_t + self.omega_t * self.O_sell_t) / (8 + self.omega_t * self.O_sell_t) + \
        #                 (self.beta * abs(self.I) if self.I < 0 else 0)
        self.pb_buy_t = (self.b_t + self.omega_t) / (8 + self.omega_t) + \
                        (self.beta * self.I if self.I > 0 else 0)
        self.pb_sell_t = (self.s_t + self.omega_t) / (8 + self.omega_t) + \
                         (self.beta * abs(self.I) if self.I < 0 else 0)

    def disp_effect(self, p_t):
        if self.p_sell == 0 and self.p_buy == 0:
            self.decide(p_t)
        elif self.p_sell > 0:
            self.dei_sell_pos(p_t)
        elif self.p_buy > 0:
            self.dei_buy_pos(p_t)

    def dei_sell_pos(self, p_t):
        if rand() < self.close_pb:
            self.close_sell(p_t)
        if self.debug:
            print('dei_sell_pos')
        if p_t > self.p_sell:
            if p_t - self.p_sell > self.lambd * self.p_sell:
                self.close_sell(p_t)
            else:
                self.cont_op()
        else:
            if self.p_sell - p_t > self.exp_r * self.p_sell:
                self.close_sell(p_t)
            else:
                self.cont_op()

    def dei_buy_pos(self, p_t):
        if rand() < self.close_pb:
            self.close_buy(p_t)
        if self.debug:
            print('dei_buy_pos')
        if p_t > self.p_buy:
            if p_t - self.p_buy > self.exp_r * self.p_buy:
                self.close_buy(p_t)
            else:
                self.cont_op()
        else:
            if self.p_buy - p_t > self.lambd * self.p_buy:
                self.close_buy(p_t)
            else:
                self.cont_op()

    def stop_loss(self, p_t):
        if self.p_sell == 0 and self.p_buy == 0:
            self.decide(p_t)
        elif self.p_sell > 0:
            self.stp_sell_pos(p_t)
        elif self.p_buy > 0:
            self.stp_buy_pos(p_t)

    def stp_buy_pos(self, p_t):
        if rand() < self.close_pb:
            self.close_buy(p_t)
        if self.debug:
            print('stp_buy_pos')
        if p_t > self.p_buy:
            if p_t - self.p_buy > self.exp_r * self.p_buy:
                self.close_buy(p_t)
            else:
                self.cont_op()
        else:
            if self.p_buy - p_t > self.stop_lim * self.p_buy:
                self.close_buy(p_t)
            else:
                self.cont_op()

    def stp_sell_pos(self, p_t):
        if rand() < self.close_pb:
            self.close_sell(p_t)
        if self.debug:
            print('stp_sell_pos')
        if p_t > self.p_sell:
            if p_t - self.p_sell > self.stop_lim * self.p_sell:
                self.close_sell(p_t)
            else:
                self.cont_op()
        else:
            if self.p_sell - p_t > self.exp_r * self.p_sell:
                self.close_sell(p_t)
            else:
                self.cont_op()

    def cont_op(self):
        # self.status = 0
        self.counter += 1

    def not_operate(self):
        self.status = 0
        self.p_buy = 0
        self.p_sell = 0
        self.counter = 0

    def decide(self, p_t):
        if self.debug:
            print('decide')
        self.update_prob()
        pb_b = self.pb_buy_t * (1 - self.pb_rest) / (self.pb_buy_t + self.pb_sell_t)
        pb_s = self.pb_sell_t * (1 - self.pb_rest) / (self.pb_buy_t + self.pb_sell_t)
        r = rand()
        if r < pb_b:
            self.buy(p_t)
        elif r < pb_b + pb_s:
            self.sell(p_t)
        else:
            self.not_operate()
        # if r < self.pb_buy_t:
        #     self.buy(p_t)
        # elif r > 1 - self.pb_sell_t:
        #     self.sell(p_t)
        # else:
        #     self.not_operate()

    def sell(self, p_t):
        if self.debug:
            print('sell')
        self.status = -1
        self.p_buy = 0
        self.p_sell = p_t
        self.counter = 0

    def buy(self, p_t):
        if self.debug:
            print('buy')
        self.status = 1
        self.p_buy = p_t
        self.p_sell = 0
        self.counter = 0

    def close_sell(self, p_t):
        if self.debug:
            print('close_sell')
        self.wealth *= (1 + (self.p_sell - p_t) / p_t)
        self.status = 1
        self.p_buy = 0
        self.p_sell = 0
        self.counter = 0

    def close_buy(self, p_t):
        if self.debug:
            print('close_buy')
        self.wealth *= (1 + (p_t - self.p_buy) / p_t)
        self.status = -1
        self.p_buy = 0
        self.p_sell = 0
        self.counter = 0
