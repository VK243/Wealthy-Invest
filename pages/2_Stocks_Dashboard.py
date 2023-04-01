# Libaries imported
import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from PIL import Image 
from stocksymbol import StockSymbol
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('SYM_KEY')
ss = StockSymbol(api_key)

# Alpha vantage key
alpha_key = os.environ.get('ALP_KEY')


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
pricing_data, fundamental_data, about= st.tabs(["Pricing Data", "Fundamental Data", "About"])

# Pricing Data
with pricing_data:
    st.header('Price Movements')
    
    ch_data = data
    ch_data['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    ch_data.dropna(inplace = True)
    
    annual_return = ch_data['% Change'].mean()*252*100
    stdev = np.std(ch_data['% Change'])*np.sqrt(252)
    
    a, b ,c,d = st.columns([2,1,0.5,10])
    a.markdown('Annual Return')
    b.markdown(round(annual_return,2))
    c.markdown("%")
    a.markdown('Standard Deviation')
    b.markdown(round(stdev*100,2))
    c.markdown("%")
    a.markdown('Risk Adj. Return')
    b.markdown(round(annual_return/(stdev*100),2))
    
    st.write("---")
    
    st.write(ch_data) 

# Fundamental Data    
with fundamental_data:
    st.header('Fundamental Data')
    
    blsh_url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker_name}&apikey={alpha_key}'
    r = requests.get(blsh_url)
    blsh = r.json()
    inst_url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker_name}&apikey={alpha_key}'
    r = requests.get(inst_url)
    inst = r.json()
    chfl_url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker_name}&apikey={alpha_key}'
    r = requests.get(chfl_url)
    chfl = r.json()
    
    if chfl is None or inst is None or blsh is None:
        st.markdown("No Data Found")
        
    
    else:
        bal_sheet, in_sheet, cash_fl = st.tabs(["Balance Sheet","Income Sheet","Cash Flow"])
        with bal_sheet:
            st.subheader("Balance Sheet")
            blsh = pd.Series(blsh)
            if len(blsh) == 0:
                st.markdown("No Data Found for Balance Sheet")
                
            else:
                an = pd.DataFrame(blsh[1])
                qu = pd.DataFrame(blsh[2])
                annual,quater = st.tabs(['Annual Reports','Quarterly Reports'])
                with annual:
                    st.dataframe(an)
                with quater:
                    st.dataframe(qu)
        
        with in_sheet:
            st.subheader("Income Statement")
            inst = pd.Series(inst)
            if len(inst) == 0:
                st.markdown("No Data Found for Income statement")
                
            else:
                an = pd.DataFrame(inst[1])
                qu = pd.DataFrame(inst[2])
                annual,quater = st.tabs(['Annual Reports','Quarterly Reports'])
                with annual:
                    st.dataframe(an)
                with quater:
                    st.dataframe(qu)
        
        with cash_fl:
            st.subheader("Cash Flow")
            chfl = pd.Series(chfl)
            if len(chfl) == 0:
                st.markdown("No Data Found for Cash Flow")
                
            else:
                an = pd.DataFrame(chfl[1])
                qu = pd.DataFrame(chfl[2])
                annual,quater = st.tabs(['Annual Reports','Quarterly Reports'])
                with annual:
                    st.dataframe(an)
                with quater:
                    st.dataframe(qu)
    
    
    
    
# About the Stock    
with about:
    stock_info = yf.Ticker(str(ticker_name)).info
    
    co1,co2 =st.columns(2)
    
    co1.header(stock_info['longName'])
    co2.markdown('## ')
    co2.metric(label=stock_info['shortName'],value=stock_info['regularMarketPrice'],delta=stock_info['regularMarketChangePercent'])
    co2.markdown('## ')
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
 
 
