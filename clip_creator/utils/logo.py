import yfinance as yf
import requests
import os

class TickerLogo:
    
    def __init__(self, ticker):
        self.ticker = ticker  # Store ticker symbol
    
    def get_logo_from_clearbit(self, website):
        if not website:
            return None
        domain = website.replace("https://www.", "").replace("http://www.", "").replace("https://", "").replace("http://", "").split("/")[0]
        return f"https://logo.clearbit.com/{domain}"

    def download_and_save_logo(self, save_dir="logos"):
        try:
            stock = yf.Ticker(self.ticker)
            website = stock.info.get("website", "")
            logo_url = self.get_logo_from_clearbit(website)
            if not logo_url:
                return None
            
            os.makedirs(save_dir, exist_ok=True)
            img_path = os.path.join(save_dir, f"{self.ticker}.png")
            
            response = requests.get(logo_url, timeout=5)
            if response.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Saved logo for {self.ticker} at {img_path}")
                return img_path
            else:
                print(f"❌ Failed to download logo for {self.ticker}")
                return None
        except Exception as e:
            print(f"⚠️ Error for {self.ticker}: {e}")
            return None

# ---------------- Example usage ----------------
logo = TickerLogo("CI")
logo.download_and_save_logo()
