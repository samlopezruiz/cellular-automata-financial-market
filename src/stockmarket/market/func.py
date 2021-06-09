from src.stockmarket.analyze.statstics import stats_kpi
from src.stockmarket.board.floor import ExchangeFloor
from src.stockmarket.market.exchange import MarketExchange
from src.stockmarket.plotly.plot import plot_price_returns
from src.stockmarket.utils.results import get_results, save_vars


def run_sim(model_cfg, in_cfg):
    market_exchange = MarketExchange(model_cfg, in_cfg)
    exchange_floor = ExchangeFloor(market_exchange, model_cfg, in_cfg, patch_size=10)
    exchange_floor.run_sime(n_iter=model_cfg['n_iter'], watch=in_cfg['watch'])
    price_hist, returns, i_hist, d_hist, watch = get_results(exchange_floor)
    if in_cfg['save_results']:
        save_vars((price_hist, returns, i_hist, d_hist, watch, model_cfg), file_path=['results', 'sim'])
    return price_hist, returns, i_hist, d_hist, watch


def eval_sim(model_cfg, in_cfg, plot=False, i=0, only_png=True):
    price_hist, returns, i_hist, d_hist, watch = run_sim(model_cfg, in_cfg)
    hurst, bjl, params, arch_vol, std_price, std_returns = stats_kpi(price_hist, returns)
    omega, alpha, beta = params['omega'], params['alpha[1]'], params['beta[1]']
    if plot:
        plot_price_returns(price_hist, returns, arch_vol, model_cfg, in_cfg, 'SIM',
                           hurst, bjl, params, only_png, suffix=i)
    return hurst, bjl, omega, alpha, beta, std_price, std_returns