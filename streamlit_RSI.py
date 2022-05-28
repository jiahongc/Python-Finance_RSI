import streamlit as st
import altair as alt
import pandas as pd
import pandas_ta as ta
import numpy as np
from IPython.display import display_html
from itertools import chain,cycle
import yfinance as yf

col1,col2 = st.columns(2)
ticker="SPY"
time="ytd"

with col1:
    ticker = st.text_input('Enter Ticker: ')

with col2:
    time = st.selectbox("Select Time", ("1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"))


df = yf.Ticker(ticker).history(period=time)
df=df.reset_index()
df['Date']=pd.to_datetime(df['Date'])
df=df[['Date','Open','High','Low','Close']]
df['Close']=df['Close']
df['RSI']=ta.rsi(df['Close'], timeperiod=14)

df.drop(range(0,14),inplace=True)
df.reset_index(drop=True,inplace=True)
df['Overbought']=70
df['Oversold']=30

Stock = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(color="grey",size=15)).encode(
    x='Date:T',
    y='Close:Q',
    tooltip=[alt.Tooltip('date:T', format='%m/%d'),
             alt.Tooltip('Close:Q', format=',.2f')]
).properties(
    title='Stock Price',
    width=800,
    height=300
)
RSI = alt.Chart(df).mark_line().encode(
    x='Date:T',
    y='RSI:Q',
    tooltip=[alt.Tooltip('date:T', format='%m/%d'),
             alt.Tooltip('Close:Q', format=',.2f'),
             alt.Tooltip('RSI:Q', format=',.2f')]
).properties(
    title='RSI',
    width=800,
    height=300)

Oversold = alt.Chart(df).mark_line(color= 'red').encode(
    x='Date:T',
    y='Oversold:Q'
)

Overbought = alt.Chart(df).mark_line(color= 'green').encode(
    x='Date:T',
    y='Overbought:Q'
)

RSI_Chart=RSI+Oversold+Overbought

with col1:
    st.altair_chart(Stock)

with col2: 
    st.altair_chart(RSI_Chart)