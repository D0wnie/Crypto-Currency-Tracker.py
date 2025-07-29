import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="Crypto Tracker", page_icon="📈", layout="centered")
st.title("📈 Crypto Price Tracker")

# --- API Functions ---
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": crypto_id, "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data[crypto_id]["usd"]

def get_price_history(crypto_id, days=1):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

# --- Crypto List ---
cryptos = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Dogecoin": "dogecoin",
    "Solana": "solana",
    "Cardano": "cardano"
}

# --- UI Controls ---
coin_name = st.selectbox("Choose a cryptocurrency:", list(cryptos.keys()))
coin_id = cryptos[coin_name]

time_range = st.selectbox("Show price history for:", ["1 Day", "7 Days", "30 Days"])
days_lookup = {"1 Day": 1, "7 Days": 7, "30 Days": 30}
days = days_lookup[time_range]

# --- Live Price ---
price = get_crypto_price(coin_id)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if price:
    st.metric(label=f"{coin_name} Current Price", value=f"${price:,}")
    st.caption(f"Last updated: {timestamp}")
else:
    st.error("Failed to load current price.")

# --- Historical Chart ---
st.subheader(f"{coin_name} Price History ({time_range})")

with st.spinner("Loading chart..."):
    history_df = get_price_history(coin_id, days=days)
    st.line_chart(history_df["price"])
