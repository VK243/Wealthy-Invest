import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
from keras.models import load_model
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from PIL import Image

# Loading Image using PIL
title_icon = Image.open('images/stock_icon.png')

st.set_page_config(
    layout="wide",
    page_title="Predict",
    page_icon=title_icon,)

st.title ("Stock Trend Prediction")

stock_input = st.text_input("Enter Stock ", 'AAPL')

df = yf.Ticker(stock_input).history(period='10y').reset_index()
st.write("---")

with st.expander("View more Data"):
    if st.checkbox("Show Data Description",value=True):
        st.write(df.describe())

    if st.checkbox("Show Raw Data",value=True):
        st.dataframe(df)
st.write("---")   

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Closing Price vs timechart')
    st.markdown("## ")
    st.markdown("## ")
    fig0 = plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    st.pyplot(fig0)
    st.write("---") 

with col2:
    st.subheader('Closing Price vs timechart with 100 days Moving Average')
    ma100 = df.Close.rolling(100).mean()
    fig1 = plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    plt.plot(ma100)
    st.pyplot(fig1)
    st.write("---") 

with col3:
    st.subheader('Closing Price vs timechart with 200 days Moving Average')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig2 = plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    plt.plot(ma100)
    plt.plot(ma200)
    st.pyplot(fig2)
    st.write("---") 

# Spliting Data into training and testing data
data_train = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_test = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

# Scaling the data using minmaxscaler
scaler = MinMaxScaler(feature_range=(0,1))
data_train_arr = scaler.fit_transform(data_train)

 # Loading the model
model = load_model('model/keras_model.h5')


past_100d = data_train.tail(100)
final_df = past_100d.append(data_test, ignore_index = True)
input_data = scaler.fit_transform(final_df)


x_test = []
y_test = []
for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test = np.array(x_test)
y_test = np.array(y_test)

y_predict = model.predict(x_test)

scaler_value = scaler.scale_
scale_fact = 1/scaler_value[0]
y_predict = y_predict * scale_fact
y_test = y_test * scale_fact


st.subheader("Prediction Value vs Original Value")
fig3 = plt.figure(figsize=(12,6))
plt.plot(y_test, label="Original Price")
plt.plot(y_predict, label="Predicted Price")
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig3)


st.write("---")
