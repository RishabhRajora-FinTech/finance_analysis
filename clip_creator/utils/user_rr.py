from random_stock_selection import TickerSelector
from logo import TickerLogo

selector = TickerSelector(exclude_file="exclude.txt")
try:
    random_tickers = selector.get_random_tickers(region="India", n=1)
    print("Random Tickers:", random_tickers)
except ValueError as e:
    print(e)
random_tickers = random_tickers[0] +".NS"
logo = TickerLogo(random_tickers)
logo.download_and_save_logo()
