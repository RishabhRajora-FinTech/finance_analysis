import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data["Close"].dropna()

def get_stock_info(ticker):

    try:
        stock_info = yf.Ticker(ticker).info
        stock_name = stock_info.get("longName", "")
    except:
        stock_name = ""

    return stock_name


import pandas as pd
def simulate_lumpsum(data, amount):
    import pandas as pd

    # Make sure it's a clean 1D Series (not DataFrame or multi-column)
    if isinstance(data, pd.DataFrame):
        if 'Close' in data.columns:
            data = data['Close']
        else:
            # fallback: take first column
            data = data.iloc[:, 0]

    data = data.dropna()

    initial_price = float(data.iloc[0])
    shares_bought = amount / initial_price
    portfolio_value = data * shares_bought

    df = pd.DataFrame({
        "Portfolio Value": portfolio_value,
        "Invested": [amount] * len(portfolio_value)
    }, index=portfolio_value.index)

    return shares_bought, float(portfolio_value.iloc[-1]), df


def simulate_sip(data, monthly_amount):
    investment = 0
    total_shares = 0
    results = []

    # Get monthly investment dates
    for date in pd.date_range(data.index[0], data.index[-1], freq="MS"):
        if date not in data.index:
            # Get nearest next available date
            future_dates = data[data.index > date]
            if not future_dates.empty:
                date = future_dates.index[0]
            else:
                continue

        price = float(data.loc[date])
        shares = monthly_amount / price
        total_shares += shares
        investment += monthly_amount
        value = total_shares * float(data.loc[date])
        results.append((date, investment, value))

    df = pd.DataFrame(results, columns=["Date", "Invested", "Value"]).set_index("Date")
    return df
