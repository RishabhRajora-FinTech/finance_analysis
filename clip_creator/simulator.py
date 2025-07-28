import yfinance as yf
import pandas as pd
import copy
import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    
    def get_stock_info(self):

        try:
            stock_info = yf.Ticker(self.ticker).info
            stock_name = stock_info.get("longName", "")
        except:
            stock_name = ""

        return stock_name


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
        years = len(df) / 365.4  # Approximate number of years based on daily data
        logging.info(f"Final value: {final_value}, Total invested: {total_invested}, Years: {years}")
        cagr = ((((final_value / total_invested) ** (1 / years)) - 1)) 
        logging.info(f"CAGR: {cagr:.6f}")       # Decimal format
        logging.info(f"CAGR (%): {cagr*100:.2f}%")  # Percent format

        desc = self.description()
        return final_value, total_invested, cagr, df, desc
    
    def description(self):
        df = self.data
        desc = {
            "ticker": self.ticker,
            "start_year": self.start_year,
            "daily_investment": self.daily_investment,
            "data_available": self.data is not None,
            "data_length": len(df),
            "start_date": df.index.min() if not df.empty else None,
            "end_date": df.index.max() if not df.empty else None,
            "final_value": df['Portfolio Value'].iloc[-1] if not df.empty else None,
            "total_invested": df['Total Invested'].iloc[-1] if not df.empty else None,
            "Duration": len(df) / 365.4,  # Approximate number of years based on daily data
            "cagr": ((((df['Portfolio Value'].iloc[-1] / df['Total Invested'].iloc[-1]) ** (1 / (len(df) / 252))) - 1)) * 100 if not df.empty else None
        }
        return desc
        