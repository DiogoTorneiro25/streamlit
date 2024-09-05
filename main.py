import streamlit as st
import pandas as pd
import yfinance as yf

# criar a interface do streamlit
@st.cache_data
def load_data(company):
    dados_acao = yf.Ticker(company)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao[["Close"]]
    return cotacoes_acao

dados = load_data("ITUB4.SA")
print(dados)

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