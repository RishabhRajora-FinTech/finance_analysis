import streamlit as st
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

# Function to fetch Reliance stock data
def fetch_reliance_data():
    try:
        stock_data = yf.download('RELIANCE.NS', start='2020-01-01', end='2023-01-01')
        if stock_data.empty:
            st.error("Failed to fetch data. Please check the ticker symbol or try again later.")
        return stock_data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

# Function to calculate returns
def calculate_returns(data):
    if data is not None and not data.empty:
        if 'Close' in data.columns:
            data['Returns'] = (data['Close'].pct_change())*100
        else:
            st.error("'Adj Close' column not found in the data.")
    return data
# Streamlit app
st.title('Reliance Stock Price and Returns Analysis')
# st.write(data.head())  # Display the first few rows of the DataFrame
# st.write(data.columns)  # Display the column names
# Fetch and display data
data = fetch_reliance_data()
data1 = data
data1.reset_index(inplace=True)  # Ensure the index is reset

if data is not None and not data.empty:
    data = calculate_returns(data)
    st.subheader('Reliance Stock Return')

    st.line_chart(data['Returns'])
    st.subheader('Reliance Stock Price')
    st.bar_chart(data1['Close'])
    st.subheader('TEST CHART')

    st.bar_chart(chart_data)
else:
    st.error("No data available to display.")