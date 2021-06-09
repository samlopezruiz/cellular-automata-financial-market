import os
import os
import warnings

import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler

from src.stockmarket.analyze.plot import plot_norm_histogram, plot_price_n_returns
from src.stockmarket.analyze.statstics import stat_test, auto_arima, arima_garch, stats_kpi
from src.stockmarket.plotly.plot import plot_price_returns
import seaborn as sns
sns.set_theme()
sns.set_context("poster", font_scale=1.2)

warnings.filterwarnings("ignore")
plt.rc("figure", figsize=(16, 12))
plt.rc("savefig", dpi=90)
plt.rc("font", family="sans-serif")
plt.rc("font", size=14)


if __name__ == '__main__':
    dataset_name = 'SIM'
    save_results = False
    #%% LOAD DATA
    # returns, price_hist = get_es_day_data()
    # price_hist = price_hist['ESc']

    #%% LOAD DATA
    # file_name = 'sim_2021_05_07_15-44'
    file_name = 'sim_2021_05_14_15-39'
    # file_name = 'sim_2021_05_14_16-29'
    # file_name = 'sim_2021_05_14_16-42'
    path = os.path.join('..', 'sim', 'results', 'good', file_name + '.z')
    price_hist, returns, i_hist, d_hist, watch, model_cfg = joblib.load(path)
    returns = np.array(returns)

    hurst, bjl, garch_params, arch_vol, std_price, std_returns, norm = stats_kpi(price_hist, returns)
    title = 'Exchange Floor Celullar Automata Simulation'
    plot_price_returns(price_hist, returns, arch_vol, model_cfg, save_results,
                       title, hurst, bjl, garch_params, std_price, std_returns, norm)
    #%%

    c_returns = returns[~np.isnan(returns)]
    # plot_price_n_returns(price_hist, c_returns, dataset_name, save_results)

    #%%

    ss = StandardScaler()
    norm_returns = ss.fit_transform(c_returns.reshape(-1, 1))

    name = 'LOG RETURNS'
    plot_norm_histogram(norm_returns)
    stat_test(returns, name, file_name=dataset_name, save=save_results)

    #%% ARIMA
    # smodel = auto_arima(returns, max_p=8, max_q=8)
    # order = smodel.order
    #%%
    # order
    arima_order = (2, 0, 2)
    garch_order = (1, 1)
    arima_garch(returns, arima_order, garch_order, dataset_name, save_results)





