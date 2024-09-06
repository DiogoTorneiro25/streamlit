# import libraries
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import timedelta

# create a function to load data
@st.cache_data
def load_data(companies):
    data = pd.DataFrame()
    for company in companies:
        dados_acao = yf.Ticker(company)
        cotacoes_acao = dados_acao.history(period="1d", start="2016-01-01", end="2024-07-01")
        cotacoes_acao = cotacoes_acao["Close"].rename(company)
        data = pd.concat([data, cotacoes_acao], axis=1)
    # Remove timezone information from index
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    return data

@st.cache_data
def load_stocks_tickers():
    all_tickers = pd.read_csv("stocks_information.csv", sep=";")
    tickers = list(all_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

# Load data
#stocks = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
stocks = load_stocks_tickers()
df = load_data(stocks)
#print(data.sort_index())
print(df)

st.write("""
    # Stock Prices
    This graph highlights the stock price evolution over the time
    """)

# Sidebar for filters
st.sidebar.header("Filters")

# Stocks filters
stocks_list = st.sidebar.multiselect("Choose the stocks to evaluate", df.columns)
if stocks_list:
        df = df[stocks_list]
        if len(stocks_list) == 1:
            single_stock = stocks_list[0]
            df = df.rename(columns={single_stock: "Close"})

# Date filters
start_date = df.index.min().to_pydatetime()
end_date = df.index.max().to_pydatetime()

# Remove timezone from the slider range dates
range_date = st.sidebar.slider(
     "Select the period",
     min_value=start_date,
     max_value=end_date,
     value=(start_date, end_date),
     step=timedelta(days=1)
)

## By doing this, the graph will only show the selected dates available in the sidebar
df = df.loc[range_date[0]:range_date[1]]

# Create line chart
st.line_chart(df)

# Filter out stocks that contain NaN values during the selected period, those should be seen in the selected period as were not available and 
# also should not be taken into consideration regarding the overall wallet performance
df = df.dropna()

# Ensure that the wallet performance calculations are done only on valid data (no NaNs)
stock_performance_text = ""

# when no stock is selected, the performance of all stocks are highlighted 
if len(stocks_list) == 0:
     stocks_list = list(df.columns)
elif len(stocks_list) == 1:
     df = df.rename(columns={"Close": single_stock})

# for simplicity lets assume that we put 1k in each of the values selected
wallet = [1000 for stock in stocks_list]
# compute the wallet starting position
initial_position_wallet = sum(wallet)

# represent the performance of each stock
for i, stock in enumerate(stocks_list):
     stock_performance = df[stock].iloc[-1] / df[stock].iloc[0] -1
     stock_performance = float(stock_performance)

     wallet[i] = wallet[i] * (1 + stock_performance)

    # format the performance of each stock with colors
     if stock_performance > 0:
          stock_performance_text = stock_performance_text + f"  \n{stock}: :green[{stock_performance:.1%}]"
     elif stock_performance < 0:
          stock_performance_text = stock_performance_text + f"  \n{stock}: :red[{stock_performance:.1%}]"
     else:
          stock_performance_text = stock_performance_text + f"  \n{stock}: {stock_performance:.1%}"

# compute the wallet final position
final_position_wallet = sum(wallet)
wallet_performance = final_position_wallet / initial_position_wallet - 1

# format the performance of each stock with colors
if wallet_performance > 0:
          wallet_performance_text = f"In this period, whe wallet overall performance is: :green[{wallet_performance:.1%}]"
elif wallet_performance < 0:
          wallet_performance_text = f"In this period, whe wallet overall performance is: :red[{wallet_performance:.1%}]"
else:
          wallet_performance_text = f"In this period, whe wallet overall performance is: :{wallet_performance:.1%}"

# Show stock performance markdown
st.write(f"""
### Stocks Performance
This was the performance of each stock during the selected period
    
{stock_performance_text}

{wallet_performance_text}
    """)