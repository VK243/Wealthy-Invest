import streamlit as st 
import pandas as pd
import numpy as np
from stocksymbol import StockSymbol
from PIL import Image
import requests
from streamlit_lottie import st_lottie
import yfinance as yf
import os



# Loading Image using PIL
title_icon = Image.open('images/stock_icon.png')

st.set_page_config(
    layout="wide",
    page_title="Wealthy Invest",
    page_icon=title_icon,)

# Remove the streamlit icon and menubar
hide_default_format = """<style>#MainMenu {visibility: hidden; }footer {visibility: hidden;}</style>"""
st.markdown(hide_default_format, unsafe_allow_html=True)


st.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
""",unsafe_allow_html=True)

@st.cache_resource
def load_website(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

landing_img = load_website('https://assets2.lottiefiles.com/packages/lf20_kuhijlvx.json')
stock_img = load_website('https://assets2.lottiefiles.com/packages/lf20_hxXmZsjAZj.json')
crypto_img = load_website('https://assets5.lottiefiles.com/packages/lf20_O1b0iWuPju.json')
predict_img = load_website('https://assets7.lottiefiles.com/packages/lf20_2iHYnjnXho.json')

# API called for list of stock-symbols
api_key = os.environ.get('SYM_KEY')
ss = StockSymbol(api_key)



col1,col2,col3 = st.columns([1,6,6])
with col2:
    st.markdown("##   ")
    st.markdown("##   ")
    st.title("Wealthy Invest")
    st.markdown("##   ")
    st.markdown("##   ")
    st.markdown("**Welcome to Wealthy Invest**, your ultimate destination for investing in stocks and cryptocurrencies. We are dedicated to providing you with the knowledge, tools, and resources you need to make informed investment decisions and achieve your financial goals. Our mission is to empower individuals like you to take control of your finances and grow your wealth with confidence. Join our community today and start your journey to financial freedom!")
with col3:
    st_lottie(landing_img,height=400)


st.write("---")

col1, col2 = st.columns([1,2])
# Create the stocks section with more detailed content
with col2:
    st.header("Stocks")
    
    st.write("Looking to invest your money and grow your wealth? At our platform, we offer the tools and information you need to make informed investment decisions in the stock and cryptocurrency markets. Join us today and start making smart investments that pay off big time!")
    st.markdown("## ")
    c1,c2,c3 = st.columns(3)
    
    msft_info = yf.Ticker('MSFT').info
    tsla_info = yf.Ticker('TSLA').info
    rel_info = yf.Ticker('RELIANCE.NS').info
    c1.metric(label = msft_info['longName'], value = msft_info['regularMarketPrice'], delta =msft_info['regularMarketChangePercent'])
    c2.metric(label = rel_info['longName'], value = rel_info['regularMarketPrice'], delta =rel_info['regularMarketChangePercent'])
    c3.metric(label = tsla_info['longName'], value = tsla_info['regularMarketPrice'], delta =tsla_info['regularMarketChangePercent'])

    st.markdown("## ")

    
with col1:
    # Add an image for visual interest
    st_lottie(stock_img,height=400)


st.write("---")

col1,col2 = st.columns([2,1])

# Create the crypto section with more detailed content
with col1:
    st.header("Crypto")

    st.write("Are you interested in investing in cryptocurrencies but don't know where to start? At our platform, we have all the information and resources you need to make smart investment decisions in the ever-growing world of cryptocurrencies. From expert advice to the latest market insights, we've got you covered. Join us today and start building your crypto portfolio with confidence!")
    
    st.markdown("## ")
    c1,c2,c3 = st.columns(3)
    
    bit_info = yf.Ticker('BTC-USD').info
    eth_info = yf.Ticker('ETH-USD').info
    tet_info = yf.Ticker('USDT-USD').info
    
    c1.metric(label = bit_info['longName'], value = bit_info['regularMarketPrice'], delta =bit_info['regularMarketChangePercent'])
    c2.metric(label = eth_info['longName'], value = eth_info['regularMarketPrice'], delta =eth_info['regularMarketChangePercent'])
    c3.metric(label = tet_info['longName'], value = tet_info['regularMarketPrice'], delta =tet_info['regularMarketChangePercent'])
    
    st.markdown("## ")

        
        
with col2:
        st_lottie(crypto_img,height=400)
    # Add an image for visual interest
    
    
# Add a separator to visually separate the sections
st.markdown("---")
col1,col2 = st.columns([1,2])
# Create the prediction section
with col2:
    st.header("Predictions")

    st.markdown("## ")

    # st.image("prediction_image.jpg", use_column_width=True) # Add an image for visual interest
    st.write("Get ahead of the game with our cutting-edge prediction tools for stocks and cryptocurrencies. With our innovative algorithms and expert analysis, you can predict market trends and stay one step ahead of the competition. Join our platform today and start predicting stock and crypto prices with confidence!")

    st.markdown("## ")
    st.markdown("## ")

    
with col1:
    st_lottie(predict_img, height=400)
    
st.write("---")    
st.markdown("## ")
c1,c2,c3 = st.columns([1,2,1])
st.markdown("## ")
with c1:

    st.markdown("## By **Varshith Kumar**")


st.markdown(
    """
    <style>
    a.icon {
        display: inline-block;
        margin-right: 1.5rem;
        padding = 30px
        font-size: 2rem;
    }
    .icon:hover {
        color: #555555;
    }
    </style>
    """
    , unsafe_allow_html=True
)

with c3:
    st.markdown("## ")
    st.markdown(
        """
        <a class=icon href="https://www.linkedin.com/in/iam-vk/" >
            <i class="fa-brands fa-2xl fa-linkedin"></i>
        </a>
        <a class=icon href="https://github.com/VK243">
            <i class="fa-brands fa-2xl fa-github"></i>
        </a>
        <a class=icon href="mailto:varshithkumar243@gmail.com">
            <i class="fa-solid fa-2xl fa-envelope" ></i>
        </a>
        """
        , unsafe_allow_html=True
    )
    st.markdown("## ")
    st.markdown("@2023 Wealthy Invest")
st.write("---")



