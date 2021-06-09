from copy import copy
from itertools import product

import pandas as pd

from src.stockmarket.harness.repeat import repeat_eval


def gs_get_cfgs(gs_cfg, model_cfg, comb=True):
    keys = list(gs_cfg.keys())
    ranges = list(gs_cfg.values())
    combinations = list(product(*ranges))
    name_cfg = copy(gs_cfg)

    cfgs_gs, names = [], []
    if comb:
        for comb in combinations:
            new_cfg = copy(model_cfg)
            for k, key in enumerate(keys):
                new_cfg[key] = comb[k]
                name_cfg[key] = comb[k]
            cfgs_gs.append(new_cfg)
            names.append(str(name_cfg))
    else:
        for i in range(len(gs_cfg[keys[0]])):
            new_cfg = copy(model_cfg)
            for key in keys:
                new_cfg[key] = gs_cfg[key][i]
                name_cfg[key] = gs_cfg[key][i]
            cfgs_gs.append(new_cfg)
            names.append(str(name_cfg))

    return cfgs_gs, names


def gs_search(gs_cfg, in_cfg, model_cfg, n_repeat=1):
    cfgs, names = gs_get_cfgs(gs_cfg, model_cfg, comb=True)

    gs_logs = []
    for c, (cfg, name) in enumerate(zip(cfgs, names)):
        print(name)
        res = repeat_eval(n_repeat, cfg, in_cfg, plot=False)
        gs_logs.append((name, res))

    stats = consolidate_log(gs_logs)
    return gs_logs, stats


def consolidate_log(gs_logs):
    stats = []
    for name, log_cfg in gs_logs:
        for hurst, bjl, omega, alpha, beta, std_price, std_returns in log_cfg:
            stats.append((str(name), hurst, bjl, omega, alpha, beta, std_price, std_returns))

    df = pd.DataFrame(stats, columns=['cfg', 'Hurst', 'BLj', 'Omega', 'Alpha', 'Beta', 'Price_Std', 'Return_Std'])
    return df