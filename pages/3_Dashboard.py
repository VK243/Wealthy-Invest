# Libaries imported
import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from PIL import Image 
from stocksymbol import StockSymbol
import os

# API called for list of stock-symbols
api_key = 'c0995e59-5689-45df-b000-352beab46454'
ss = StockSymbol(api_key)


# Streamlit config page
title_icon = Image.open('images/stock_icon.png')
st.set_page_config(
    layout="wide",
    page_title="Dashboard",
    page_icon=title_icon,)

@st.cache_resource
def load_sym():
    symbol_list_in = ss.get_symbol_list(market="IN")
    symbol_list_us = ss.get_symbol_list(market="US")
    df_in = pd.DataFrame(symbol_list_in)
    df_us = pd.DataFrame(symbol_list_us)
    df_in = df_in[['symbol', 'shortName', 'longName', 'exchange', 'market', 'quoteType']]
    df_us = df_us[['symbol', 'shortName', 'longName', 'exchange', 'market', 'quoteType']]
    stocks_df = pd.concat([df_in, df_us], ignore_index=True)
    return stocks_df


# Page Content
st.title("Dashboard")  # Title
col1, col2 = st.columns(2) # Making two columns
stocks_data = load_sym() # Loading the stocks data

# Column 1 for ticker values and dates
# Create a list of longName with exchange
longName_exchange_list = [f"{row['longName']} ({row['exchange']})" for _, row in stocks_data.iterrows()]

ticker = col1.selectbox('Select a stock:', options=longName_exchange_list, index=0)
ticker_name = stocks_data.loc[stocks_data['longName'] + ' (' + stocks_data['exchange'] + ')' == ticker, 'symbol'].iloc[0]

c1,c2 = col1.columns(2)

start_date = c1.date_input("Start Date")
end_date = c2.date_input("End Date")

data = yf.download(ticker_name,start_date,end_date)

fig = px.line(data, x=data.index, y='Adj Close', title=ticker_name)
col2.plotly_chart(fig)

# Tabs for the additional data about the stocks
pricing_data, fundamental_data, about = col1.tabs(["Pricing Data", "Fundamental Data", "About"])

# Pricing Data
with pricing_data:
    st.header('Price Movements')
    
    ch_data = data
    ch_data['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    ch_data.dropna(inplace = True)
    
    annual_return = ch_data['% Change'].mean()*252*100
    stdev = np.std(ch_data['% Change'])*np.sqrt(252)
    
    a, b ,c = st.columns([2,1,1])
    a.markdown('Annual Return')
    b.markdown(round(annual_return,2))
    c.markdown("%")
    a.markdown('Standard Deviation')
    b.markdown(round(stdev*100,2))
    c.markdown("%")
    a.markdown('Risk Adj. Return')
    b.markdown(round(annual_return/(stdev*100),2))
    
    st.write("---")
    
    st.dataframe(ch_data) 

# Fundamental Data    
with fundamental_data:
    st.header('Fundamental Data')
    
    
    
# About the Stock    
with about:
    stock_info = yf.Ticker(str(ticker_name)).info
    
    co1,co2 =st.columns(2)
    
    co1.header(stock_info['longName'])
    pchange = ((stock_info['regularMarketPrice'] - stock_info['regularMarketPreviousClose']) / stock_info['regularMarketPreviousClose']) * 100
    co2.metric(label=stock_info['shortName'],value=stock_info['regularMarketPrice'],delta=stock_info['regularMarketChangePercent'])
    
    a, b ,c, d = st.columns(4)
    a.markdown('##### **Qoute Type**')
    b.markdown(stock_info['quoteType'])
    a.markdown('##### **Symbol**')
    b.markdown(stock_info['symbol'])
    a.markdown('##### **Exchange**')
    b.markdown(stock_info['fullExchangeName'])
    a.markdown('##### **Currency**')
    b.markdown(stock_info['financialCurrency'])
    a.markdown('##### **Market State**')
    b.markdown(stock_info['marketState'])
    a.markdown('##### **Region**')
    b.markdown(stock_info['region'])
    
    c.markdown('##### **Open**')
    d.markdown(stock_info['regularMarketOpen'])
    c.markdown('##### **High**')
    d.markdown(stock_info['regularMarketDayHigh'])
    c.markdown('##### **Low**')
    d.markdown(stock_info['regularMarketDayLow'])
    c.markdown('##### **Close**')
    d.markdown(stock_info['regularMarketPreviousClose'])
    c.markdown('##### **Volume**')
    d.markdown(stock_info['regularMarketVolume'])
    c.markdown('##### **Change**')
    d.markdown(stock_info['regularMarketChange'])
    