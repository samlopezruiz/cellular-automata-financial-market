import datetime
import joblib
import pandas as pd
from src.stockmarket.timeseries.process import get_returns
import os


def get_results(exchange_floor):
    watch = exchange_floor.watch
    price_hist = exchange_floor.price_hist
    i_hist = exchange_floor.i_hist
    d_hist = exchange_floor.d_hist
    returns = get_returns(price_hist)
    return price_hist, returns, i_hist, d_hist, watch


def save_vars(vars, file_path):
    if file_path is None:
        file_path = ['results', 'result']
    print("saving .z")
    if not os.path.exists(file_path[0]):
        os.makedirs(file_path[0])
    path = file_path[:-1].copy() + [file_path[-1] + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".z"]
    joblib.dump(vars, os.path.join(*path))
