import streamlit as st
import altair as alt
import pandas as pd
import pandas_ta as ta
import numpy as np
# from itertools import chain,cycle
import yfinance as yf

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'><em>Stock Research</em></h1>   \n", unsafe_allow_html=True)
st.markdown("   \n")
st.markdown("   \n")
st.markdown("   \n")
st.markdown("   \n")
col1,col_placeholder,col2 = st.columns([3,1,3])
with col1:
    ticker = st.text_input('Enter Ticker: ')
    time = st.selectbox("Select Time", ("1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"))
    metrics= st.selectbox("Select Financial Table",("Financials","Quarterly Financials",
 "Balance Sheet","Quarterly Balance Sheet"
    ,"Cashflow","Quarterly Cashflow","Earnings","Quarterly Earnings"))

if ticker and time:
    df = yf.Ticker(ticker).history(period=time)
    df=df.reset_index()
    df['Date']=pd.to_datetime(df['Date'])
    df=df[['Date','Open','High','Low','Close']]
    # df['Close']=np.round(df['Close'],2)
    df['RSI']=ta.rsi(df['Close'], timeperiod=14)

    # df=df.drop(range(0,14))
    df.dropna(inplace=True)
    df=df.reset_index(drop=True)
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
    ).interactive()
    RSI = alt.Chart(df).mark_line().encode(
        x='Date:T',
        y='RSI:Q',
        tooltip=[alt.Tooltip('date:T', format='%m/%d'),
                alt.Tooltip('Close:Q', format=',.2f'),
                alt.Tooltip('RSI:Q', format=',.2f')]
    ).properties(
        title='RSI',
        width=800,
        height=300).interactive()

    Oversold = alt.Chart(df).mark_line(color= 'red').encode(
        x='Date:T',
        y='Oversold:Q'
    )

    Overbought = alt.Chart(df).mark_line(color= 'green').encode(
        x='Date:T',
        y='Overbought:Q'
    )

    RSI_Chart=RSI+Oversold+Overbought

    with col2:
        st.altair_chart(Stock)
        st.altair_chart(RSI_Chart)

if ticker and metrics:
    company = yf.Ticker(ticker)
    if metrics=="Financials":
        df_company = company.financials
    elif metrics=="Quarterly Financials":
        df_company = company.quarterly_financials
    elif metrics=="Balance Sheet":
        df_company = company.balance_sheet
    elif metrics=="Quarterly Balance Sheet":
        df_company = company.quarterly_balance_sheet
    elif metrics=="Cashflow":
        df_company = company.cashflow
    elif metrics=="Quarterly Cashflow":
        df_company = company.quarterly_cashflow
    elif metrics=="Earnings":
        df_company = company.earnings
    elif metrics=="Quarterly Earnings":
        df_company = company.quarterly_earnings
    elif metrics=="":
        df_company = company
    elif metrics=="":
        df_company = company
    
    with col2:
        st.write(metrics + " for " + ticker)
        st.dataframe(df_company)
