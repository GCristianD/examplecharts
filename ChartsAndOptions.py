import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout="wide")

path = 'AAPLOptionChain'
with open(path, 'rb') as handle:
    expdates, callsDic, putsDic = pickle.load(handle)

st.header('Option chain')

col1, col2 = st.columns(2)
with col1:
    optype = st.radio(
            "Select option",
            key="option",
            options=["Calls", "Puts"] )
with col2:
    expdate = st.selectbox(
            "Date of expiration:", expdates)


st.write('Display AAPL strikes between 160 and 200:')

if optype=='Calls':
    st.table(callsDic[expdate].drop(columns=['contractSymbol']))
else:
    st.table(putsDic[expdate].drop(columns=['contractSymbol']))   




