import yfinance as yf
import json
import pandas as pd
import ta
import time

# deneme = yf.Ticker("THYAO.IS")
# keys = ["regularMarketPrice", "marketCap", "enterpriseValue", "52WeekChange", "earningsQuarterlyGrowth", "totalCash", "totalCashPerShare", "freeCashflow","earningsGrowth","fiftyTwoWeekLowChangePercent", "fiftyTwoWeekHighChangePercent", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "fiftyDayAverage", "twoHundredDayAverage", "averageDailyVolume3Month", "fiftyDayAverageChange", "twoHundredDayAverageChange"]
# values = {k: deneme.info.get(k) for k in keys}
# balance = deneme.quarterly_balance_sheet
# income = deneme.quarterly_income_stmt  

#print(values)
# dat.calendar
# dat.analyst_price_targets

# Hisse verisini al (örnek: ASELS.IS)
#ticker = "THYAO.IS"
#df = yf.Ticker(ticker).history(period="6mo", interval="1d")

# Teknik göstergeleri hesapla
#df['rsi'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
#macd = ta.trend.MACD(close=df['Close'])
#df['macd'] = macd.macd()
#df['macd_signal'] = macd.macd_signal()
#bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
#df['bb_bbm'] = bb.bollinger_mavg()
#df['bb_bbh'] = bb.bollinger_hband()
#df['bb_bbl'] = bb.bollinger_lband()
#df["SMA_5"] = df["Close"].rolling(window=5).mean()
#df["SMA_10"] = df["Close"].rolling(window=10).mean()
#df["EMA_5"] = df["Close"].ewm(span=5).mean()

# df['Date'] = df['Date'].astype(str)  # Eğer datetime formatındaysa, önce string'e çevir
# df['Date'] = df['Date'].apply(lambda x: x.split(' ')[0])  # ' ' karakterine göre ayır ve ilk kısmı al


# Boş verileri temizle
#df.dropna(inplace=True)

# Özellikler ve hedef sütunu
#features = df[['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm', 'bb_bbh', 'bb_bbl', 'SMA_5', 'SMA_10', 'EMA_5']]
#target = df['Close']
#last_week = df.iloc[-8:-1][['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm', 'bb_bbh', 'bb_bbl', 'SMA_5', 'SMA_10', 'EMA_5']]
#last_data = df.iloc[-1][['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm', 'bb_bbh', 'bb_bbl', 'SMA_5', 'SMA_10', 'EMA_5']]
#second_data = df.iloc[-2][['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm', 'bb_bbh', 'bb_bbl', 'SMA_5', 'SMA_10', 'EMA_5']]
#son10_rsi = df[['rsi']].iloc[-10:].copy()
#son10_rsi.index = son10_rsi.index.strftime('%Y-%m-%d')
#print(son10_rsi)
# rsi 30 altı aşırı satım 70 üstü aşırı alım eğer 30 üstü çıkarsa alım zamanı 70 in altını kırarsa satım zamanı
def rsi_signal(df):
    son10_rsi = df[['rsi']].iloc[-10:].copy()
    son10_rsi.index = son10_rsi.index.strftime('%Y-%m-%d')  # Tarihi sadeleştir

    rsi_text = "\n".join([f"{date}: {value:.2f}" for date, value in son10_rsi['rsi'].items()])

    last_rsi = df['rsi'].iloc[-1]
    second_last_rsi = df['rsi'].iloc[-2]

    if 30 < last_rsi < 70 and last_rsi > second_last_rsi:
        trend = "RSI Trend: Positive"
    elif last_rsi > 70 and second_last_rsi > last_rsi:
        trend = "RSI Trend: Negative (Overbought Reversal)"
    elif last_rsi < 30 and last_rsi > second_last_rsi:
        trend = "RSI Trend: Positive (Oversold Reversal)"
    else:
        trend = "RSI Trend: Negative"

    return f"{trend}\nLast 10 RSI values:\n{rsi_text}"  

def macd_signal(macd, signal):
    if signal > macd:
        return False
    if signal < macd:
        return True

def bol_signal(l_price, bbm):
    if l_price > bbm:
        return True
    if l_price < bbm:
        return False


def stock_info(stock):
    data = yf.Ticker(stock+".IS")
    time.sleep(2)
    df = yf.Ticker(stock+".IS").history(period="6mo", interval="1d")
    keys = ["regularMarketPrice", "marketCap", "enterpriseValue", "52WeekChange", "totalCash", "totalCashPerShare", "cashFlow", "freeCashflow","earningsGrowth","fiftyTwoWeekLowChangePercent", "fiftyTwoWeekHighChangePercent", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "fiftyDayAverage", "twoHundredDayAverage", "averageDailyVolume3Month", "fiftyDayAverageChange", "twoHundredDayAverageChange"]
    values = {k: data.info.get(k) for k in keys}

    marketcap = values['marketCap']

    df['rsi'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
    macd = ta.trend.MACD(close=df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['bb_bbm'] = bb.bollinger_mavg()

    last_data = df.iloc[-1][['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm']]
    second_data = df.iloc[-2][['Open', 'High', 'Low', 'Volume', 'rsi', 'macd', 'macd_signal', 'bb_bbm']]

    rsi_sig = rsi_signal(df=df)
    macd_sig = macd_signal(last_data['macd'], last_data['macd_signal'])
    bol_sig = bol_signal(values['regularMarketPrice'], last_data['bb_bbm'])

    balance = data.quarterly_balance_sheet
    income = data.quarterly_income_stmt    

    return values, rsi_sig, macd_sig, bol_sig

#print(stock_info("THYAO"))
