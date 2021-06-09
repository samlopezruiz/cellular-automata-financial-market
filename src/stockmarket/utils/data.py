import os
import pandas as pd
from src.stockmarket.timeseries.process import get_returns


def get_es_day_data(freq='day'):
    file_name = 'ES 2012-2020.csv'
    if freq == 'day':
        path = 'D:\MEGA\Proyectos\Trading\Algo_Trading\Historical_Data\compressed\day\ES\data'
    elif freq == 'min':
        path = 'D:\MEGA\Proyectos\Trading\Algo_Trading\Historical_Data\compressed\minute\ES\data'
    price_hist = pd.read_csv(os.path.join(path, file_name))
    returns = get_returns(price_hist['ESc'])

    if freq == 'min':
        returns = returns[-10000:]
        price_hist = price_hist[-10000:]
    return returns, price_hist['ESc']