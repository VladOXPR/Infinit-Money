import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use("dark_background")

ma_1 = 12
ma_2 = 26

symbol = 'BTC'
data = yf.download(symbol, period='1y', interval='1d')

data[f'MA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
data[f'MA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

data = data.iloc[ma_2:]

buy_signals = []
sell_signals = []
trigger = 1
balance = 10000


for x in range(len(data)):
    share_price = data['Adj Close'].iloc[x]

    if data[f'MA_{ma_1}'].iloc[x] > data[f'MA_{ma_2}'].iloc[x] and trigger != -1:
        buy_signals.append(data['Adj Close'].iloc[x])
        sell_signals.append(float('nan'))
        trigger = -1
        print('Bought', share_price)
        balance = balance - share_price
        print('Balance', balance)

    elif data[f'MA_{ma_1}'].iloc[x] < data[f'MA_{ma_2}'].iloc[x] and trigger != 1:
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[x])
        trigger = 1
        print('Sold ', share_price)
        balance = balance + share_price
        print('Balance', balance)

    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))


data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

plt.plot(data['Adj Close'], label="Share Price", color="white")
plt.plot(data[f'MA_{ma_1}'], label=f'MA_{ma_1}', color="orange", linestyle="--")
plt.plot(data[f'MA_{ma_2}'], label=f'MA_{ma_2}', color="yellow", linestyle="--")
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
plt.show()
