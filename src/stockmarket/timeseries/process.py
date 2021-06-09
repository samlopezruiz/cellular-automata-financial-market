import numpy as np
import pandas as pd


def get_returns(price):
    return np.array([0] + list(np.diff(np.log(price))))
    # return np.array(pd.Series(price).diff())


def hist_to_ticks(ticks, history):
    tick_series = []
    p = history[0]
    open, close, high, low = p, p, p, p
    for i, p in enumerate(history):
        if i % ticks == 0:
            close = p
            tick_series.append((open, close, high, low))
            open = p
            high = p
            low = p
        else:
            if p > high:
                high = p
            if p < low:
                low = p

    return np.array(tick_series)