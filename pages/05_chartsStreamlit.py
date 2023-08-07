import streamlit as st
import pandas as pd
import numpy as np
import json

from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(layout="wide")


df = pd.read_csv('AAPL2.csv', index_col=0)

background = st.radio("Background color:",('white', 'black'))


COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350


candles = json.loads(df.filter(['time','open','high','low','close'], axis=1).to_json(orient = "records") )


chartMultipaneOptions = [
    {
        "width": 900,
        "height": 600,
        "layout": {
            "background": {
                "type": "solid",
                "color": background
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)"
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10,
            "minBarSpacing": 8,
            "timeVisible": True,
            "secondsVisible": False,
        }
    }
]

seriesCandlestickChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": False,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR
        }
    }
]



renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesCandlestickChart
    }
])



