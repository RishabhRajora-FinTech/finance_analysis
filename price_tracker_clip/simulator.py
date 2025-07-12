import yfinance as yf
import pandas as pd
import copy


class InvestmentSimulator:
    def __init__(self, ticker: str, start_year: int, daily_investment: float = 1.0):
        self.ticker = ticker.upper()
        self.start_year = start_year
        self.daily_investment = daily_investment
        self.data = None

    def fetch_data(self):
        df = yf.download(self.ticker, start=f"{self.start_year}-01-01", interval='1d')
        df = df[['Close']].dropna()
        df = df.resample('D').ffill()
        self.data = df
        return df

    def simulate(self):
        # Step 1: Fetch if not already available
        if self.data is None:
            self.fetch_data()

        df = self.data.copy()

        # Step 2: Handle yfinance's MultiIndex columns (e.g., ('Close', 'ROST'))
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)  # Drop the first level ("Ticker")


        # Step 3: Validate 'Close' column presence
        if 'Close' not in df.columns:
            raise ValueError(f"'Close' column not found in data for {self.ticker}")

        # Step 4: Validate 'Close' column has non-null values
        if df['Close'].isnull().all():
            raise ValueError(f"All Close values are null for ticker: {self.ticker}")

        # Step 5: Ensure index is datetime and resample to daily frequency
        df.index.name = None
        df = df.resample('D').ffill()

        # Step 6: Ensure 'Investment' is a Series aligned to the index
        df['Investment'] = pd.Series(self.daily_investment, index=df.index)

        # Step 7: Perform calculations
        df['Shares'] = df['Investment'] / df['Close']
        df['Cumulative Shares'] = df['Shares'].cumsum()
        df['Portfolio Value'] = df['Cumulative Shares'] * df['Close']
        df['Total Invested'] = df['Investment'].cumsum()

        # Step 8: Save back
        self.data = df


    def get_results(self):
        if self.data is None:
            self.simulate()
        df = self.data
        final_value = df['Portfolio Value'].iloc[-1]
        total_invested = df['Total Invested'].iloc[-1]
        years = len(df) / 365.25
        cagr = ((final_value / total_invested) ** (1 / years) - 1) * 100
        return final_value, total_invested, cagr, df
