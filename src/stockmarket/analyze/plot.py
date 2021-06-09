import datetime
import os

import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, acf, plot_pacf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import acf, q_stat, adfuller
from scipy.stats import probplot, moment, norm
import matplotlib.pyplot as plt


def plot_correlogram(x, lags=None, title=None, figsize=(14, 10), file_name='plot', save=False):
    x = x[~np.isnan(x)]
    lags = min(10, len(x) // 5) if lags is None else lags
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=figsize)
    axes[0][0].plot(x)
    q_p = np.max(acorr_ljungbox(x, lags=lags)[1])
    stats = f'Box-Ljung: {np.max(q_p):>8.2f}\nADF: {adfuller(x)[1]:>11.2f}'
    axes[0][0].text(x=.02, y=.85, s=stats, transform=axes[0][0].transAxes)
    probplot(x, plot=axes[0][1])
    mean, var, skew, kurtosis = moment(x, moment=[1, 2, 3, 4])
    s = f'Mean: {mean:>12.2f}\nSD: {np.sqrt(var):>16.2f}\nSkew: {skew:12.2f}\nKurtosis:{kurtosis:9.2f}'
    axes[0][1].text(x=.02, y=.75, s=s, transform=axes[0][1].transAxes)
    plot_acf(x=x, lags=lags, zero=False, ax=axes[1][0])
    plot_pacf(x, lags=lags, zero=False, ax=axes[1][1])
    axes[1][0].set_xlabel('Lag')
    axes[1][1].set_xlabel('Lag')
    fig.suptitle(title, fontsize=20)
    fig.tight_layout()
    fig.subplots_adjust(top=.9)

    if save:
        new_dir('images')
        file_name = file_name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".png"
        plt.savefig(os.path.join('images', file_name))
    plt.show()


def new_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    # sns.distplot(norm_returns, fit=norm, kde=True)
    # plt.show()


def plot_norm_histogram(series, bins=50, scaler=0.89):
    series = series[~np.isnan(series)]
    mu, std = norm.fit(series)
    # Plot the histogram.
    plt.hist(series, bins=bins, density=True, alpha=0.6, color='gray')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'b', linewidth=2, label='Normal Distribution')

    # p = norm.pdf(x, mu, std*scaler)
    # plt.plot(x, p, 'b', linewidth=2, label='Normal Distribution')
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    plt.legend()

    plt.show()


def plot_volatility_returns(returns, volatility, file_name='plot', save=False):
    plt.plot(volatility, color='red', label='Volatility')
    plt.plot(returns, color='grey',
             label='Returns', alpha=0.4)
    plt.legend(loc='upper right')

    if save:
        new_dir('images')
        file_name = file_name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".png"
        plt.savefig(os.path.join('images', file_name))
    plt.show()


def plot_price_n_returns(p, r, fig_size=(15, 9), file_name='plot', save=False):
    fig, axes = plt.subplots(2, 1)
    axes[0].plot(p)
    axes[1].plot(r)
    if save:
        new_dir('images')
        file_name = file_name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".png"
        plt.savefig(os.path.join('images', file_name))
    plt.show()


def plot_hurst(H, c, data, file_name='plot', save=False):
    f, ax = plt.subplots()
    ax.plot(data[0], c * data[0] ** H, color="deepskyblue")
    ax.scatter(data[0], data[1], color="purple")
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Time interval')
    ax.set_ylabel('R/S ratio')
    ax.grid(True)
    if save:
        new_dir('images')
        file_name = file_name + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".png"
        plt.savefig(os.path.join('images', file_name))
    plt.show()


