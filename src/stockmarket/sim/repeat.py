import pandas as pd
from src.stockmarket.harness.repeat import repeat_eval


if __name__ == '__main__':
    in_cfg = {'n_iter': 1000, 'save_results': False, 'animate': False, 'debug': False, 'watch': [1]}
    model_cfg = {'impact': 1, 'r_max': .25, 'I_shock': 0, 'close_pb': 0.2, 'pb_rest': .2, 'p': 2000,
                 'wealth': 100, 'omega_max': 1, 'n': 3000, 'ttypes_dist': [.3, .7]}

    n_repeat = 3
    logs = repeat_eval(n_repeat, model_cfg, in_cfg, plot=True)

    df = pd.DataFrame(logs, columns=['hurst', 'bjl', 'omega', 'alpha', 'beta'])
