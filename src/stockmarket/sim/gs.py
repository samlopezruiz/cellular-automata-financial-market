import numpy as np
import seaborn as sns

from src.stockmarket.harness.gridsearch import gs_search
from src.stockmarket.plt.plot import plot_gs_stats
from src.stockmarket.utils.results import save_vars

sns.set_theme()
sns.set_context("poster", font_scale=1.2)

if __name__ == '__main__':
    in_cfg = {'save_results': False, 'animate': False, 'debug': False, 'watch': []}
    model_cfg = {'n_iter': 2000, 'impact': 1, 'r_max': .350, 'I_shock': 0, 'close_pb': 0.2,
                 'pb_rest': 0.2, 'p': 2000, 'wealth': 100, 'omega_max': 1, 'n': 3000, 'ttypes_dist': [.3, .7]}

    # gs_cfg = {'n': list(range(1000, 6000, 1000))}
    # gs_cfg = {'n_iter': list(range(1000, 6000, 1000))}
    # gs_cfg = {'r_max': list(np.round(np.arange(0.05, 0.4, 0.05), 2))}
    # gs_cfg = {'omega_max': [0.001, .01, 1, 10, 100]}
    # gs_cfg = {'ttypes_dist': [[.3, .7], [.5, .5], [.7, .3]]}

    # gs_cfg = {'close_pb': list(np.round(np.arange(0, 1, .2), 2))}
    gs_cfg = {'close_pb': list(np.round(np.arange(0, 1, .2), 2))}
    # gs_cfg = {'pb_rest': list(np.round(np.arange(0, 1, .2), 2))}
    # gs_cfg = {'impact': list(np.round(np.arange(0.5, 3, .5), 2))}
    # gs_cfg = {'close_pb': list(np.round(np.arange(0, .6, .2), 2)), 'pb_rest': list(np.round(np.arange(0, .6, .2), 2))}

    n_repeat = 7
    save = True
    gs_logs, stats = gs_search(gs_cfg, in_cfg, model_cfg, n_repeat)

    #%%
    vars = (gs_logs, stats, in_cfg, gs_cfg)
    save_vars(vars, ['gs_results', '_'.join(gs_cfg.keys())])
    #%%
    plot_gs_stats(stats, model_cfg, gs_cfg, figsize=(25, 15), save=save, save_folder='gs_images')
