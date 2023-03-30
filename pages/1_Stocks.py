import streamlit as st 
import pandas as pd
import numpy as np
from nsetools import Nse
from PIL import Image
import requests


# Loading Image using PIL
title_icon = Image.open('images/stock_icon.png')

st.set_page_config(
    layout="wide",
    page_title="Stocks",
    page_icon=title_icon,)

# Remove the streamlit icon and menubar
hide_default_format = """<style>#MainMenu {visibility: hidden; }footer {visibility: hidden;}</style>"""
st.markdown(hide_default_format, unsafe_allow_html=True)

# Object of nsetools
nse = Nse()


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('''# **Indian Stock Prices - NSE**
Real time Stocks and Index prices
''')
nse_symbols = pd.DataFrame(pd.Series(nse.get_stock_codes())).reset_index()
nse_symbols.columns = ['symbol','stockName']
nse_symbols = nse_symbols.iloc[1:]  
company_names = nse_symbols['stockName'].tolist()


@st.cache_resource
def stock_quote(sym):
    d = nse.get_quote(sym)
    return d

@st.cache_resource
def index_quote(sym):
    d = nse.get_index_quote(sym)
    return d

@st.cache_resource
def get_sym(name):
    symbol = nse_symbols.loc[nse_symbols['stockName']== name,'symbol'].iloc[0]
    return symbol


@st.cache_resource
def stock_value():
    rel = stock_quote('reliance')
    tcs =stock_quote('tcs')
    hdfc =stock_quote('HDFCBANK')
    itc = stock_quote('itc')
    infy = stock_quote('infy')
    HINDUNILVR = stock_quote('HINDUNILVR')
    NESTLEIND = stock_quote('NESTLEIND')
    ICICIBANK = stock_quote('ICICIBANK')    
    return rel,tcs,hdfc,itc,infy,HINDUNILVR,NESTLEIND,ICICIBANK
    
@st.cache_resource
def index_value():
    n50 = index_quote('nifty 50')
    nn50 = index_quote('NIFTY NEXT 50')
    nm50 = index_quote('NIFTY MIDCAP 50')
    ns100 = index_quote('NIFTY SMLCAP 100')
    n100 = index_quote('NIFTY 100')
    n200 = index_quote('NIFTY 200')
    n500 = index_quote('NIFTY 500')
    nm100 = index_quote('NIFTY MIDCAP 100')
    return n50,nn50,nm50,nm100,n100,ns100,n200,n500
    

rel,tcs,hdfc,itc,infy,HINDUNILVR,NESTLEIND,ICICIBANK = stock_value()
n50,nn50,nm50,nm100,n100,ns100,n200,n500 = index_value()

# Search Box
c1,c2,c3 = st.columns(3)

option = c3.selectbox('Search',company_names)
option_sym = get_sym(option)
option_data = stock_quote(option_sym)

c1.subheader(option_data['companyName'])
c2.metric(label=option_data['symbol'], value=option_data['lastPrice'], delta=option_data['pChange'])

# Top Stocks
st.write("---")

st.header("Top Stocks")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)

col1.write(rel['symbol'])
col2.write(tcs['symbol'])
col3.write(hdfc['symbol'])
col4.write(itc['symbol'])
col1.metric(label=rel['companyName'], value=rel['lastPrice'], delta=rel['pChange'])
col2.metric(label=tcs['companyName'], value=tcs['lastPrice'], delta=tcs['pChange'])
col3.metric(label=hdfc['companyName'], value=hdfc['lastPrice'], delta=hdfc['pChange'])
col4.metric(label=itc['companyName'], value=itc['lastPrice'], delta=itc['pChange'])
col5.write(HINDUNILVR['symbol'])
col6.write(NESTLEIND['symbol'])
col7.write(ICICIBANK['symbol'])
col8.write(infy['symbol'])
col5.metric(label=HINDUNILVR['companyName'], value=HINDUNILVR['lastPrice'], delta=HINDUNILVR['pChange'])
col6.metric(label=NESTLEIND['companyName'], value=NESTLEIND['lastPrice'], delta=NESTLEIND['pChange'])
col7.metric(label=ICICIBANK['companyName'], value=ICICIBANK['lastPrice'], delta=ICICIBANK['pChange'])
col8.metric(label=infy['companyName'], value=infy['lastPrice'], delta=infy['pChange'])


# Top Indexes
st.write("---")

st.header("Top Indexes")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)


col1.metric(label=n50['name'], value=n50['lastPrice'], delta=n50['pChange'])
col2.metric(label=nn50['name'], value=nn50['lastPrice'], delta=nn50['pChange'])
col3.metric(label=nm50['name'], value=nm50['lastPrice'], delta=nm50['pChange'])
col4.metric(label=ns100['name'], value=ns100['lastPrice'], delta=ns100['pChange'])
col5.metric(label=n100['name'], value=n100['lastPrice'], delta=n100['pChange'])
col6.metric(label=nm100['name'], value=nm100['lastPrice'], delta=nm100['pChange'])
col7.metric(label=n200['name'], value=n200['lastPrice'], delta=n200['pChange'])
col8.metric(label=n500['name'], value=n500['lastPrice'], delta=n500['pChange'])


# Top Gainers
st.write("---")

st.header("Top Gainers")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)
d = nse.get_top_gainers()
d1,d2,d3,d4,d5,d6,d7,d8= d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]
col1.metric(label=d1['symbol'], value=d1['lowPrice'], delta=d1['netPrice'])
col2.metric(label=d2['symbol'], value=d2['lowPrice'], delta=d2['netPrice'])
col3.metric(label=d3['symbol'], value=d3['lowPrice'], delta=d3['netPrice'])
col4.metric(label=d4['symbol'], value=d4['lowPrice'], delta=d4['netPrice'])
col5.metric(label=d5['symbol'], value=d5['lowPrice'], delta=d5['netPrice'])
col6.metric(label=d6['symbol'], value=d6['lowPrice'], delta=d6['netPrice'])
col7.metric(label=d7['symbol'], value=d7['lowPrice'], delta=d7['netPrice'])
col8.metric(label=d8['symbol'], value=d8['lowPrice'], delta=d8['netPrice'])


# Top Losers 
st.write("---")

st.header("Top Losers")
col1,col2,col3,col4 = st.columns(4)
d = nse.get_top_losers()
d1,d2,d3,d4 = d[0],d[1],d[2],d[3] 
col1.metric(label=d1['symbol'], value=d1['lowPrice'], delta=d1['netPrice'])
col2.metric(label=d2['symbol'], value=d2['lowPrice'], delta=d2['netPrice'])
col3.metric(label=d3['symbol'], value=d3['lowPrice'], delta=d3['netPrice'])
col4.metric(label=d4['symbol'], value=d4['lowPrice'], delta=d4['netPrice'])


# Preopen Nifty
st.write("---")

st.header("Preopen Nifty")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)
d = nse.get_preopen_nifty()
d1,d2,d3,d4,d5,d6,d7,d8= d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]
col1.metric(label=d1['symbol'], value=d1['iep'], delta=d1['perChn'])
col2.metric(label=d2['symbol'], value=d2['iep'], delta=d2['perChn'])
col3.metric(label=d3['symbol'], value=d3['iep'], delta=d3['perChn'])
col4.metric(label=d4['symbol'], value=d4['iep'], delta=d4['perChn'])
col5.metric(label=d5['symbol'], value=d5['iep'], delta=d5['perChn'])
col6.metric(label=d6['symbol'], value=d6['iep'], delta=d6['perChn'])
col7.metric(label=d7['symbol'], value=d7['iep'], delta=d7['perChn'])
col8.metric(label=d8['symbol'], value=d8['iep'], delta=d8['perChn'])


# Preopen Bank Nifty
st.write("---")

st.header("Preopen Nifty Banks")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)
d = nse.get_preopen_niftybank()
d1,d2,d3,d4,d5,d6,d7,d8= d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]
col1.metric(label=d1['symbol'], value=d1['iep'], delta=d1['perChn'])
col2.metric(label=d2['symbol'], value=d2['iep'], delta=d2['perChn'])
col3.metric(label=d3['symbol'], value=d3['iep'], delta=d3['perChn'])
col4.metric(label=d4['symbol'], value=d4['iep'], delta=d4['perChn'])
col5.metric(label=d5['symbol'], value=d5['iep'], delta=d5['perChn'])
col6.metric(label=d6['symbol'], value=d6['iep'], delta=d6['perChn'])
col7.metric(label=d7['symbol'], value=d7['iep'], delta=d7['perChn'])
col8.metric(label=d8['symbol'], value=d8['iep'], delta=d8['perChn'])


# Preopen FO Stocks
st.write("---")

st.header("Preopen FO Stocks")
col1,col2,col3,col4 = st.columns(4)
col5,col6,col7,col8 = st.columns(4)
d = nse.get_preopen_fno()
d1,d2,d3,d4,d5,d6,d7,d8= d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7]
col1.metric(label=d1['symbol'], value=d1['iep'], delta=d1['perChn'])
col2.metric(label=d2['symbol'], value=d2['iep'], delta=d2['perChn'])
col3.metric(label=d3['symbol'], value=d3['iep'], delta=d3['perChn'])
col4.metric(label=d4['symbol'], value=d4['iep'], delta=d4['perChn'])
col5.metric(label=d5['symbol'], value=d5['iep'], delta=d5['perChn'])
col6.metric(label=d6['symbol'], value=d6['iep'], delta=d6['perChn'])
col7.metric(label=d7['symbol'], value=d7['iep'], delta=d7['perChn'])
col8.metric(label=d8['symbol'], value=d8['iep'], delta=d8['perChn'])

st.write("---")
