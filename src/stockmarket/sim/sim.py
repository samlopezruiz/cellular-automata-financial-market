import matplotlib.pyplot as plt

from src.stockmarket.analyze.statstics import stats_kpi, correlation_test, coeff_garch, stat_test
from src.stockmarket.market.func import run_sim
from src.stockmarket.plotly.plot import plot_price_returns

# model_cfg = {'impact': 1, 'r_max': 0.15, 'I_shock': 0, 'close_pb': .1, 'pb_rest': .5, 'p': 2000,
#                  'wealth': 100, 'omega_max': .01, 'n': 2500, 'ttypes_dist': [.3, .7]}


if __name__ == '__main__':
    #%% SIM
    in_cfg = {'save_results': False, 'animate': True, 'debug': False, 'watch': []}
    model_cfg = {'n_iter': 2000, 'impact': 3, 'r_max': .35, 'I_shock': 0.1, 'close_pb': 0.01, 'pb_rest': .5,
                 'p': 2000, 'wealth': 100, 'omega_max': 1, 'n': 3000, 'ttypes_dist': [.3, .7]}

    price_hist, returns, i_hist, d_hist, watch = run_sim(model_cfg, in_cfg)
    hurst, bjl, garch_params, arch_vol, std_price, std_returns, norm = stats_kpi(price_hist, returns)

    #%% PLOT
    title = 'Exchange Floor Celullar Automata Simulation'
    plot_price_returns(price_hist, returns, arch_vol, model_cfg, in_cfg['save_results'],
                       title, hurst, bjl, garch_params,  std_price, std_returns, norm)

    name = 'LOG RETURNS'
    stat_test(returns, name, file_name='', save=False)
    #%%


    # ticks = 10
    # plotly_ticks_series(price_hist, ticks, in_cfg, title)













# #%%
#     sum_wealth = 0
#     for trader in exchange_floor.market_exchange.traders:
#         print(trader.wealth)
#         sum_wealth += trader.wealth
#
#
#     print(sum_wealth / n)
