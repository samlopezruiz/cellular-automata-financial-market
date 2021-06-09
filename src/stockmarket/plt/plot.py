import copy
import os
from datetime import datetime

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# def plot_gs_stats(df, model_cfg, gs_cfg=None, title=None, rmargin=0.7, figsize=(15, 9), save=False, save_folder='images'):
#     fig, axes = plt.subplots(1, 7, figsize=figsize)
#     sns.barplot(data=df, y='Hurst', x='cfg', capsize=.2, ax=axes[0]).set(xticklabels=[])
#     sns.barplot(data=df, y='BLj', x='cfg', capsize=.2, ax=axes[1]).set(xticklabels=[])
#     sns.barplot(data=df, y='Omega', x='cfg', capsize=.2, ax=axes[2]).set(xticklabels=[])
#     sns.barplot(data=df, y='Alpha', x='cfg', capsize=.2, ax=axes[3]).set(xticklabels=[])
#     sns.barplot(data=df, y='Beta', x='cfg', capsize=.2, ax=axes[4]).set(xticklabels=[])
#     sns.barplot(data=df, y='Price_Std', x='cfg', capsize=.2, ax=axes[5]).set(xticklabels=[])
#     sns.barplot(data=df, y='Return_Std', x='cfg', capsize=.2, ax=axes[6], hue='cfg', dodge=False).set(xticklabels=[])
#     plt.subplots_adjust(right=rmargin)
#     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#     new_cfg = copy.copy(model_cfg)
#     for key in gs_cfg.keys():
#         del new_cfg[key]
#     cfg_str = str(new_cfg)
#     if gs_cfg is not None:
#         fig.suptitle(
#             'Grid Search for: ' + str(list(gs_cfg.keys())) + '\n' + cfg_str[:len(cfg_str) // 2] + '\n' + cfg_str[len(cfg_str) // 2:])
#     if title is not None:
#         fig.suptitle(title)
#     plt.tight_layout()
#     if save:
#         create_dir(save_folder)
#         fig.savefig(os.path.join(save_folder, '_'.join(gs_cfg.keys()) + '_' + datetime.now().strftime("%d_%m_%Y %H-%M") + '.png'))
#     plt.show()


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def plot_gs_stats(df, model_cfg, gs_cfg=None, figsize=(15, 9), save=False, save_folder='images'):
    fig, axes = plt.subplots(2, 4, figsize=figsize)
    sns.barplot(data=df, y='Hurst', x='cfg', capsize=.2, ax=axes[0][0]).set(xticklabels=[])
    sns.barplot(data=df, y='BLj', x='cfg', capsize=.2, ax=axes[0][1]).set(xticklabels=[])
    sns.barplot(data=df, y='Omega', x='cfg', capsize=.2, ax=axes[1][0]).set(xticklabels=[])
    sns.barplot(data=df, y='Alpha', x='cfg', capsize=.2, ax=axes[1][1]).set(xticklabels=[])
    sns.barplot(data=df, y='Beta', x='cfg', capsize=.2, ax=axes[1][2]).set(xticklabels=[])
    sns.barplot(data=df, y='Price_Std', x='cfg', capsize=.2, ax=axes[0][2]).set(xticklabels=[])
    sns.barplot(data=df, y='Return_Std', x='cfg', capsize=.2, ax=axes[0][3]).set(xticklabels=[])
    sns.barplot(data=df, y=np.zeros(len(df['cfg'])), x='cfg', capsize=.2, ax=axes[1][3], hue='cfg', dodge=False).set(
        xticklabels=[])
    axes[1][3].axis('off')
    new_cfg = copy.copy(model_cfg)
    for key in gs_cfg.keys():
        del new_cfg[key]
    cfg_str = str(new_cfg)
    if gs_cfg is not None:
        fig.suptitle(
            'Grid Search for: ' + str(list(gs_cfg.keys())) + '\n' + cfg_str[:len(cfg_str) // 2] + '\n' + cfg_str[
                                                                                                         len(cfg_str) // 2:])
    plt.tight_layout()
    if save:
        create_dir(save_folder)
        fig.savefig(os.path.join(save_folder,
                                 '_'.join(gs_cfg.keys()) + '_' + datetime.now().strftime("%d_%m_%Y %H-%M") + '.png'))
    plt.show()