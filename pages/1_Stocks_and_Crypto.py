# Libaries imported
import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from PIL import Image 
from stocksymbol import StockSymbol
import os
from dotenv import load_dotenv

# Loading Image using PIL
title_icon = Image.open('images/stock_icon.png')

st.set_page_config(
    layout="wide",
    page_title="Stocks and Crypto",
    page_icon=title_icon,)


load_dotenv()
api_key = os.environ.get('SYM_KEY')

ss = StockSymbol(api_key)


# Remove the streamlit icon and menubar
hide_default_format = """<style>#MainMenu {visibility: hidden; }footer {visibility: hidden;}</style>"""
st.markdown(hide_default_format, unsafe_allow_html=True)


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


def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a



st.title("Stocks")

stocks_data = load_sym() # Loading the stocks data

col1, col2, col3 = st.columns([2,1,2])
# Create a list of longName with exchange
longName_exchange_list = [f"{row['longName']} ({row['exchange']})" for _, row in stocks_data.iterrows()]

ticker = col1.selectbox('Select a stock:', options=longName_exchange_list, index=0)
ticker_name = stocks_data.loc[stocks_data['longName'] + ' (' + stocks_data['exchange'] + ')' == ticker, 'symbol'].iloc[0]

stock_info = yf.Ticker(str(ticker_name)).info
with col3:
    st.header(stock_info['longName'])
    st.markdown('## ')
    st.metric(label=stock_info['shortName'],value=stock_info['regularMarketPrice'],delta=stock_info['regularMarketChangePercent'])
    st.markdown('## ')


st.write('---')
st.title("Crypto")

crypto_df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')

co1, co2, co3 = st.columns([2,1,2])
selection = co1.selectbox("Select the Crypto:",crypto_df.symbol,list(crypto_df.symbol).index('BTCBUSD'))

sel = crypto_df[crypto_df.symbol == selection]

sel_price = round_value(sel.weightedAvgPrice)

sel_per = f'{float(sel.priceChangePercent)}%'
with co3:
    st.markdown('## ')
    st.metric(selection,sel_price,sel_per)
    st.markdown('## ')
    
st.write('---')