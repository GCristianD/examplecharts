import streamlit as st
import pandas as pd

import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")


dff = pd.read_csv('AAPL.csv', index_col=0)
dff['date'] = mdates.date2num(pd.DatetimeIndex(dff.index).to_pydatetime())



data = dff[['date', 'Open', 'High', 'Low', 'Close']][-200:].values
df = dff[-200:]
figsize=(12,9)
color = 'lightgray'
ticker = 'AAPL'

fig, (axis1, axis2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]},figsize=figsize)

axis1 = fig.add_subplot(211)
candlestick_ohlc(axis1, data, width=0.7, colorup='g', colordown='r')
axis1.plot(df['date'],df['EMA_8'], label='EMA 8', color='red')
axis1.plot(df['date'],df['EMA_21'], label='EMA 21', color='orange')
axis1.plot(df['date'],df['EMA_34'], label='EMA 34', color='yellow')
axis1.plot(df['date'],df['SMA_50'], label='SMA 50', color='green')
axis1.plot(df['date'],df['SMA_100'], label='SMA 100', color='blue')
axis1.plot(df['date'],df['SMA_200'], label='SMA 200', color='violet')
axis1.legend(loc='upper left')
axis1.set_title(f"{ticker} stock")
axis1.xaxis_date()
axis1.set_facecolor(color)

axis2 = fig.add_subplot(212)
axis2.set_ylim(-10, 110)
axis2.plot(df["%K"], color="tab:blue") # fast
axis2.plot(df["%D"], color="tab:orange") # slow
axis2.axhline(60, color="tab:red", ls="--")
axis2.axhline(40, color="tab:green", ls="--")
axis2.legend(["%K", "%D"], loc="upper left")
axis2.set_title("Stochastic Oscillator ({8}-day)")
axis2.set_facecolor(color)


st.pyplot(fig=fig, clear_figure=None, use_container_width=True)

