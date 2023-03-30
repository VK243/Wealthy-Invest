import streamlit as st 
from streamlit_option_menu import option_menu
st.set_page_config(
    layout="wide",
    page_title="Mutual Funds",
    page_icon="wallet2",)

selected = option_menu(
        menu_title=None,
        options = ["Home", "Stocks", "Mutual Funds", "Crypto"],
        icons = ["house","cash","wallet2","currency-bitcoin"], 
        menu_icon="cast",
        default_index=0,
        orientation= "horizontal"
    )
