from hurst import compute_Hc

from src.stockmarket.analyze.statstics import correlation_test, coeff_garch
from src.stockmarket.utils.data import get_es_day_data

if __name__ == '__main__':
    #%%
    # file_name = 'sim_2021_05_12_09-45'
    # path = os.path.join('..', 'sim', 'results', file_name + '.z')
    # price_hist, returns, i_hist, d_hist, watch, model_cfg = joblib.load(path)
    #%%
    returns, price_hist = get_es_day_data()
    hurst_res = compute_Hc(price_hist, kind='price', simplified=True)
    bjl = correlation_test(returns, print_=False)

    print("Hurst={:.4f}, Box-Ljung={:.4f}".format(hurst_res[0], bjl))

    #%%
    params, _ = coeff_garch(returns)
    omega, alpha, beta = params['omega'], params['alpha[1]'], params['beta[1]']
    print('Garch: σ2t = {:.2} + {:.2} ϵ2t + {:.2} σ2t−1'.format(omega, alpha, beta))

    #%%
    # The larger the α , the bigger the immediate impact of the shock
    # The larger the β , the longer the duration of the impact
    # GARCH(1,1):σ2t=ω+αϵ2t−1+βσ2t−1
    # Intuitively, GARCH variance forecast can be interpreted as a weighted average of three different variance forecasts.
    #
    # One is a constant variance that corresponds to the long run average.
    # The second is the new information that was not available when the previous forecast was made.
    # The third is the forecast that was made in the previous period.
    # The weights on these three forecasts determine how fast the variance changes with new information and how fast it reverts to its long run mean.