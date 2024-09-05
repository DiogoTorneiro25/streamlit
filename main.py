# import libraries
import yfinance as yf
import pandas as pd
import streamlit as st


# create a function to load data
@st.cache_data
def load_data(companies):
    tickers_text = " ".join(companies)
    dados_acao = yf.Ticker(tickers_text)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    print(cotacoes_acao)
    cotacoes_acao = cotacoes_acao[["Close"]]
    return cotacoes_acao

stocks = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]

# prepare visualizations
data = load_data(stocks)
print(data)

st.write("""
# Stock Prices
This graph highlights the stock price evolution over the time
""") # markdown

# create line chart
st.line_chart(dados)

# criar a interface do streamlit
st.write("""
# Fim do App
""") # markdown