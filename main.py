# import libraries
import yfinance as yf
import pandas as pd
import streamlit as st


# create a function to load data
@st.cache_data
def load_data(companies):
    data = pd.DataFrame()
    for company in companies:
        #tick_text = " ".join(company)
        dados_acao = yf.Ticker(company)
        cotacoes_acao = dados_acao.history(period="1d", start="2016-01-01", end="2024-07-01")
    #print(cotacoes_acao)
        cotacoes_acao = cotacoes_acao["Close"].rename(company)
        data = pd.concat([data, cotacoes_acao], axis=1)
    return data

stocks = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
data = load_data(stocks)

# prepare visualizations and filters
stocks_list = st.multiselect("Choose the stocks to evaluate",data.columns)
if stocks_list:
    data = data[stocks_list]
    if len(stocks_list) == 1:
        single_stock = stocks_list[0]
        data = data.rename(columns={single_stock: "Close"})
        
#print(lista_acoes)

st.write("""
# Stock Prices
This graph highlights the stock price evolution over the time
""") # markdown

# create line chart
st.line_chart(data)

# criar a interface do streamlit
st.write("""
# End of App
""") # markdown