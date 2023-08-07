import streamlit as st
import pandas as pd
import numpy
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.linear_model import LinearRegression
import numpy as np
import math

#################################
#################################
#################################

st.set_page_config(layout="wide")


def make_charts_Bull(df, ticker, showchannel = True):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.012, subplot_titles=(ticker,"Stochastic Oscillator"), shared_xaxes=True, row_heights=[0.6, 0.1])

    fig.add_trace(go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], name='Rainbow') ,row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['EMA_8'], line=dict(color='red', width=1), name="EMA8") , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['EMA_21'], line=dict(color='orange', width=1), name="EMA21"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['EMA_34'], line=dict(color='yellow', width=1), name="EMA34") , row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['SMA_50'], line=dict(color='green', width=1), name="SMA50"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['SMA_100'], line=dict(color='blue', width=1), name="SMA100"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.Date, y=df['SMA_200'], line=dict(color='violet', width=2), name="SMA200"), row=1, col=1)

    if showchannel == 'Yes':
        dtest = df.iloc[-84:]
        mindate = dtest[dtest['Low'] == dtest['Low'].min()]['Date'].iloc[0]
        mindateloc = dtest[dtest['Low'] == dtest['Low'].min()].index[0]
        lastdate = dtest['Date'].iloc[-1]

        dreg = dtest.loc[mindateloc:].drop(columns='Date')
        dreg = dreg.reset_index()
        X = dreg['index'].values.reshape(-1, 1)  
        Y = dreg['Close'].values.reshape(-1, 1)  
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        Y_pred = linear_regressor.predict(X)
        RSS = np.sum(np.square(Y - Y_pred))
        rse = math.sqrt(RSS / (len(Y) - 2))
        
        
        fig.add_trace(go.Scatter(x=[mindate,lastdate], y=[Y_pred[0][0], Y_pred[-1][0]], line=dict(color='gray', width=1)) , row=1, col=1)
        fig.add_trace(go.Scatter(x=[mindate,lastdate], y=[Y_pred[0][0]+2*rse, Y_pred[-1][0]+2*rse], line=dict(color='black', width=1)) , row=1, col=1)
        fig.add_trace(go.Scatter(x=[mindate,lastdate], y=[Y_pred[0][0]-2*rse, Y_pred[-1][0]-2*rse], line=dict(color='black', width=1)) , row=1, col=1)
        #fig.add_trace(go.Scatter(x=[mindate,lastdate], y=[Y_pred[0][0]-1.5 *rse,Y_pred[-1][0]-1.5 *rse], line=dict(color='gray', width=1), fill='tonexty') , row=1, col=1)

    
    fig.add_trace(go.Scatter(
             x=df.Date,
             y=df["%D"], line=dict(color='orange', width=2), name="%K (Slow)"), row=2, col=1)
    fig.add_hline(y=60, line_width=2, line_dash="dash", line_color="red",row=2, col=1)
    fig.add_hline(y=40, line_width=2, line_dash="dash", line_color="green",row=2, col=1)


    fig.update_layout(height=800) 
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])


    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ]),
            type="date"),#end xaxis  definition

        xaxis1_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        xaxis2_type="date"
        );

    return fig


showchannel = st.radio("Show trend:",('Yes', 'No'))


df = pd.read_csv('SLF.csv', index_col=0)
df = df[-200:]
df.reset_index(inplace=True)
ticker = 'SLF'
fig = make_charts_Bull(df, ticker, showchannel = showchannel)
st.plotly_chart(fig,theme=None, use_container_width=True)
