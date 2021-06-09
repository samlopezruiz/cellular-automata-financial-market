from multiprocessing import cpu_count
from joblib import Parallel, delayed
from src.stockmarket.market.func import eval_sim


def repeat_eval(n_repeat, model_cfg, in_cfg, parallel=True, plot=False):
    if parallel:
        executor = Parallel(n_jobs=cpu_count(), backend='multiprocessing')
        tasks = (delayed(eval_sim)(model_cfg, in_cfg, plot, i=i) for i in range(n_repeat))
        logs = executor(tasks)
    else:
        logs = []
        for _ in range(n_repeat):
            best_ind, best_gen, best_eval, log = eval_sim(model_cfg, in_cfg, plot)
            logs.append((best_gen, best_eval, log, best_ind))
    return logs
