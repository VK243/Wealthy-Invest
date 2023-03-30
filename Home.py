import streamlit as st 
from PIL import Image

# Loading Image using PIL
title_icon = Image.open('images/stock_icon.png')

st.set_page_config(
    layout="wide",
    page_title="Stocks",
    page_icon=title_icon,)