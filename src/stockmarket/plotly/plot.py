import time
import pandas as pd
import os
from datetime import date
import datetime
import numpy as np
from plotly import graph_objects as go
from plotly.subplots import make_subplots

from src.stockmarket.plotly.utils import get_title
from src.stockmarket.timeseries.process import hist_to_ticks, get_returns


def plotly_time_series(df, title=None, save=False, legend=True, file_path=None, size=(1980, 1080),
                       markers='lines+markers', xaxis_title="time", markersize=3, label_scale=1,
                       alphas=None, only_png=False):
    features = df.columns
    rows = list(range(len(features)))
    if alphas is None:
        alphas = [1 for _ in range(len(features))]
    n_rows = len(set(rows))

    f = len(features)
    fig = make_subplots(rows=n_rows, cols=1, shared_xaxes=True)

    for i in range(f):
        df_ss = df[features[i]].dropna()
        fig.append_trace(
            go.Scatter(
                x=df_ss.index,
                y=df_ss,
                visible=True,
                showlegend=legend,
                name=features[i],
                mode=markers,
                marker=dict(size=markersize),
                opacity=alphas[i]
            ),
            row=rows[i] + 1,
            col=1
        )
        if i == n_rows - 1:
            fig['layout']['xaxis' + str(i + 1)]['title'] = xaxis_title

    for i in range(f):
        fig['layout']['yaxis' + str(i + 1)]['title'] = features[i]
    fig.update_layout(template="plotly_white", xaxis_rangeslider_visible=False,
                      title=title, legend=dict(font=dict(size=18 * label_scale)))

    fig.update_xaxes(tickfont=dict(size=14 * label_scale), title_font=dict(size=18 * label_scale))
    fig.update_yaxes(tickfont=dict(size=14 * label_scale), title_font=dict(size=18 * label_scale))

    fig.show()
    time.sleep(1.5)

    if file_path is not None and save is True:
        plotly_save(fig, file_path, size, only_png)
    return fig


def plotly_save(fig, file_path, size, only_png=True):
    print("saving .html and .png")
    if not os.path.exists(file_path[0]):
        os.makedirs(file_path[0])
    image_path = file_path[:-1].copy() + [
        file_path[-1] + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".png"]
    if size is None:
        size = (1980, 1080)
    fig.write_image(os.path.join(*image_path), width=size[0], height=size[1])
    if not only_png:
        html_path = file_path[:-1].copy() + [
            file_path[-1] + '_' + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + ".html"]
        fig.write_html(os.path.join(*html_path))



def plotly_traces_candles(df_ss, features, type_plot=None, title=None, save=False,
                          legend=True, file_path=None, size=(1980, 1080),
                          markers='lines+markers', xaxis_title="time", markersize=3, label_scale=1,
                          alphas=None):

    f = len(features)
    heights = [0.3 / f for _ in range(f)]
    heights.insert(0, 0.7)
    if type_plot is None:
        type_plot = ["line" for _ in range(f)]

    fig = make_subplots(rows=f+1, cols=1, shared_xaxes=True, row_heights=heights)

    fig.append_trace(
        go.Candlestick(
            x=df_ss.index,
            open=df_ss['open'],
            high=df_ss['high'],
            low=df_ss['low'],
            close=df_ss['close'],
            visible=True,
            showlegend=False
        ),
        row=1,
        col=1
    )

    for i in range(f):
        fig.append_trace(
            go.Bar(
                x=df_ss.index,
                y=df_ss[features[i]],
                orientation="v",
                visible=True,
                showlegend=False,
            ) if type_plot[i] == 'bar' else
            go.Scatter(
                x=df_ss.index,
                y=df_ss[features[i]],
                visible=True,
                showlegend=False,
                marker_color='rgba(0, 0, 200, 1)',
                marker=dict(size=markersize,),
            ),
            row=i + 2,
            col=1
        )

    fig['layout']['yaxis1']['title'] = "Price"
    for i in range(f):
        fig['layout']['yaxis' + str(i + 2)]['title'] = features[i]

    fig.update_layout(template="plotly_white", xaxis_rangeslider_visible=False,
                      title=title, legend=dict(font=dict(size=18 * label_scale)))

    fig.update_xaxes(tickfont=dict(size=14 * label_scale), title_font=dict(size=18 * label_scale))
    fig.update_yaxes(tickfont=dict(size=14 * label_scale), title_font=dict(size=18 * label_scale))


    fig.show()
    time.sleep(1.5)

    if file_path is not None and save is True:
        plotly_save(fig, file_path, size)
    return fig


def plotly_ticks_series(price_hist, ticks, in_cfg, title, type_plot=None):
    ticks_ts = hist_to_ticks(ticks, price_hist)
    df = pd.DataFrame(ticks_ts, columns=['open', 'close', 'high', 'low'])
    df['returns'] = get_returns(df['close'])
    plotly_traces_candles(df, ['returns'], title=title+' Ticks: '+str(ticks), type_plot=type_plot,
                          save=in_cfg['save_results'], file_path=['images', 'sim_candles'], )


def plot_price_returns(price_hist, returns, arch_vol, model_cfg, save_results, title, hurst, bjl,
                       garch_params, std_price, std_returns, norm, only_png=False, suffix=None):
    title = get_title(title, model_cfg, hurst, bjl, garch_params, std_price, std_returns, norm)
    data = np.array([price_hist, returns, arch_vol]).T
    df = pd.DataFrame(data, columns=['Price', 'Returns', 'Volatility'])
    plotly_time_series(df, title=title, markers='lines+markers',
                       save=save_results, file_path=['images', 'sim_r'+str(suffix)], only_png=only_png)