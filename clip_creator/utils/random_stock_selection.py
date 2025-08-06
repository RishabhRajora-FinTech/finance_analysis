import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TickerSelector:
    def __init__(self, exclude_file="exclude.txt"):
        self.exclude_file = exclude_file
        self.excluded_tickers = self._load_excluded_tickers()

    def _load_excluded_tickers(self):
        """Load excluded tickers from a file."""
        try:
            with open(self.exclude_file, "r") as f:
                return [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            print("No exclude.txt found. Proceeding with no exclusions.")
            return []

    def _get_us_tickers(self):
        """Fetch US tickers from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url)[0]
        return table['Symbol'].tolist()


    def _get_india_tickers(self):
        """Fetch India tickers from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/NIFTY_50"
        table = pd.read_html(url)[1]  # NIFTY table is the second one
        logging.info("Columns in the NIFTY 50 table: %s", table.columns)  # Logging the columns
        # Adjust the column name based on the actual structure
        return table['Symbol'].tolist()  # Replace 'Symbol' with the correct column name
    
    def _get_uk_tickers(self):
        """Fetch UK tickers from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
        table = pd.read_html(url)[3]  # FTSE 100 company table
        return table['EPIC'].tolist()

    def _get_europe_tickers(self):
        """Fetch Europe tickers from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
        table = pd.read_html(url)[1]
        return table['Ticker'].tolist()

    def get_random_tickers(self, region="US", n=1):
        """Get random tickers from a specified region."""
        region = region.lower()
        if region == "us":
            tickers = self._get_us_tickers()
        elif region == "india":
            tickers = self._get_india_tickers()
        elif region == "uk":
            tickers = self._get_uk_tickers()
        elif region == "europe":
            tickers = self._get_europe_tickers()
        else:
            raise ValueError(f"Unknown region: {region}")
        logging.info(f"Ticker List for exclude tickers, {excluded_tickers}")
                # Filter out excluded tickers
        tickers = [
            ticker for ticker in tickers
            if ticker.split('.')[0].upper() not in self.excluded_tickers
        ]
        
        if len(tickers) < n:
            raise ValueError(f"Not enough tickers to choose from after exclusions. Only {len(tickers)} available.")

        return random.sample(tickers, n)
    


# # Example usage
# if __name__ == "__main__":
#     selector = TickerSelector(exclude_file="exclude.txt")
#     try:
#         random_tickers = selector.get_random_tickers(region="India", n=1)
#         print("Random Tickers:", random_tickers)
#     except ValueError as e:
#         print(e)