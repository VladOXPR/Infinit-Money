import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


# Data setup
symbol = 'BTC'
data = yf.download(symbol, period='1y', interval='1d')
data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['EMA12'] - data['EMA26']
data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']


# Variables
in_position = False
sell_executed = False
buy_price = 0
sell_price = 0
buy_dates = []
sell_dates = []
balance = 10000
shares = 1


# Algorithm
print('Your Balance is', balance)
for i in range(len(data)):
    if data['MACD_Histogram'].iloc[i] > 0 and data['MACD_Histogram'].iloc[i] > data['MACD_Histogram'].iloc[i - 1] and not in_position:
        print(f"Buy at {data['Close'].iloc[i]}")
        buy_price = data['Close'].iloc[i]
        buy_dates.append(data.index[i])
        in_position = True
        sell_executed = False
        balance = balance - buy_price * shares
    elif data['MACD_Histogram'].iloc[i] < data['MACD_Histogram'].iloc[i - 1] and in_position:
        print(f"Sell at {data['Close'].iloc[i]}")
        sell_price = data['Close'].iloc[i]
        sell_dates.append(data.index[i])
        in_position = False
        sell_executed = True
        balance = balance + sell_price * shares
if in_position:
    print(f"Sell at {data['Close'].iloc[-1]}")
    sell_dates.append(data.index[-1])
print('Your Balance is', balance)


# Plotting
plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))
ax1.plot(data.index, data['Close'], label='Close Price', color='white')
ax1.plot(data.index, data['EMA12'], label='12-day EMA', color='orange', linestyle="--")
ax1.plot(data.index, data['EMA26'], label='26-day EMA', color='yellow', linestyle="--")
ax1.scatter(buy_dates, data.loc[buy_dates, 'Close'], marker='o', color='green', label='Buy')
ax1.scatter(sell_dates, data.loc[sell_dates, 'Close'], marker='o', color='red', label='Sell')
ax1.set_ylabel('Price')
ax1.legend()
ax2.plot(data.index, data['MACD'], label='MACD', color='cyan')
ax2.plot(data.index, data['Signal_Line'], label='Signal Line', color='magenta')
ax2.bar(data.index, data['MACD_Histogram'], color=np.where(data['MACD_Histogram'] > 0, 'g', 'r'))
ax2.axhline(0, linestyle='--', color='gray')
ax2.set_xlabel('Date')
ax2.set_ylabel('MACD')
ax2.legend()
plt.show()
