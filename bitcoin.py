import streamlit as st
import pandas as pd
import requests
import plotly.express as px

days = st.slider('No of days', 1, 365, 90)
currency = st.radio(
    "Currency",
    ('cad', 'usd', 'inr'))
API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={}&days={}&interval=daily'.format(
    currency, days)
req = requests.get(API_URL)
if req.status_code == 200:
    data = req.json()

raw_data = data['prices']
date_list = []
price_list = []
for rows in raw_data:
    date_list.append(pd.to_datetime(rows[0], unit='ms'))
    price_list.append(rows[1])

df = pd.DataFrame(dict(
    Date=date_list,
    Price=price_list
))

graph = px.line(
    df,
    x="Date",
    y="Price",
    title="Line frame"
)
graph.update_traces(line_color="white")
st.plotly_chart(graph)

st.write("Average price during this time was {} {}".format(
    sum(price_list)/len(price_list), currency))
