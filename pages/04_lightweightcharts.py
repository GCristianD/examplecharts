import streamlit as st
import pandas as pd

from lightweight_charts.widgets import StreamlitChart


st.set_page_config(layout="wide")

df = pd.read_csv('AAPL3.csv', index_col=0)
dsm = df[['Date']].copy()
dsm['SMA50'] = df['Close'].rolling(50).mean()
dsm['SMA100'] = df['Close'].rolling(100).mean()
dsm['SMA200'] = df['Close'].rolling(200).mean()
ema = [8,21,34]
for x in ema: dsm["EMA_"+str(x)] = round( df['Close'].ewm(span=x).mean() , 2)
dsm.dropna(inplace=True)


chart = StreamlitChart(width=900, height=600)
#chart.legend(visible=True)

chart.set(df)

line8 = chart.create_line(color='red', price_line=False)
line21 = chart.create_line(color='orange', price_line=False)
line34 = chart.create_line(color='yellow', price_line=False)

line50 = chart.create_line(color='green', price_line=False)
line100 = chart.create_line(color='blue', price_line=False, width=1)
line200 = chart.create_line(color='violet', price_line=False)

line8.set(dsm, name='EMA_8')
line21.set(dsm, name='EMA_21')
line34.set(dsm, name='EMA_34')
line50.set(dsm, name='SMA50')
line100.set(dsm, name='SMA100')
line200.set(dsm, name='SMA200')

chart.load()
