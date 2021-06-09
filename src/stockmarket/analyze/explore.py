from src.stockmarket.analyze.plot import plot_norm_histogram
from src.stockmarket.analyze.statstics import stats_kpi
from src.stockmarket.market.func import run_sim
from src.stockmarket.plotly.plot import plot_price_returns
from hurst import random_walk
from src.stockmarket.timeseries.process import get_returns
import numpy as np
# model_cfg = {'impact': 1, 'r_max': 0.15, 'I_shock': 0, 'close_pb': .1, 'pb_rest': .5, 'p': 2000,
#                  'wealth': 100, 'omega_max': .01, 'n': 2500, 'ttypes_dist': [.3, .7]}
from src.stockmarket.utils.data import get_es_day_data

if __name__ == '__main__':
    #%% SIM
    in_cfg = {'save_results': False}
    # price_hist = np.array(random_walk(2000, proba=.2)) + 2000
    # returns = get_returns(price_hist)

    #%%
    returns, price_hist = get_es_day_data(freq='min')
    plot_norm_histogram(returns)

    #%%
    hurst, bjl, garch_params, arch_vol, std_price, std_returns, norm = stats_kpi(price_hist, returns)
    model_cfg = ''

    #%% PLOT
    title = 'ES 2012-2020'
    plot_price_returns(price_hist, returns, arch_vol, model_cfg, in_cfg['save_results'],
                       title, hurst, bjl, garch_params,  std_price, std_returns, norm, suffix='sim')



