import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import os
import shutil
from moviepy import ImageSequenceClip
# from moviepy.video.fx.resize import resize

from plotter import PlotBuilder  # 🔁 You must define this class separately


# --- Get Company Name ---
def get_stock_info(ticker):
    try:
        stock_info = yf.Ticker(ticker).info
        return stock_info.get("longName", ticker)
    except:
        return ticker


# --- Fetch Stock Data ---
def fetch_data(ticker, start="2023-01-01", end="2023-12-31", freq='M'):
    df = yf.download(ticker, start=start, end=end)[['Close']]
    df = df.resample(freq).first().dropna()
    if isinstance(df.index, pd.PeriodIndex):
        df.index = df.index.to_timestamp()
    df.index = pd.to_datetime(df.index)
    return df


# --- Compute Lump Sum and SIP Values ---
def calculate_investments(df, lump_sum_amt=10000, sip_amt=500):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)  # Drop the first level ("Ticker")



    df['Shares_Lump'] = lump_sum_amt / df.iloc[0]['Close']
    df['Value_Lump'] = df['Shares_Lump'] * df['Close']
    df['Shares_SIP'] = (sip_amt / df['Close']).cumsum()
    df['Value_SIP'] = df['Shares_SIP'] * df['Close']
    df['Total Invested'] = np.arange(1, len(df) + 1) * sip_amt
    df['Portfolio Value'] = df['Value_SIP']  # can be changed to Value_Lump
    df['Formatted_Date'] = df.index.strftime('%d-%m-%Y')
    return df


# --- Generate Frames using PlotBuilder ---
def generate_frames(df, stock_name, ticker, start_year, folder='frames'):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    for i in range(1, len(df) + 1):
        df_clip = df.iloc[:i].copy()

        # 🔁 Use PlotBuilder to generate annotated Reel plot
        plot = PlotBuilder(df_clip, ticker=ticker, start_year=start_year, name=stock_name)
        fig = plot.create_plot()

        # 🖼 Format for Instagram Reels
        fig.update_layout(width=1080, height=1920)

        frame_path = f"{folder}/frame_{i:03d}.png"
        fig.write_image(frame_path, width=1080, height=1920, scale=1)

        print(f"✅ Saved: {frame_path}")


# --- Compile Frames into MP4 Reel ---
def create_video(folder='frames', output='investment_growth_reel.mp4', fps=10):
    frames = sorted([f"{folder}/{f}" for f in os.listdir(folder) if f.endswith(".png")])
    clip = ImageSequenceClip(frames, fps=fps)
    # clip = clip.fx(resize, (1080, 1920))  # Ensure 9:16 size
    clip.write_videofile(output, codec='libx264', audio=False)
    print(f"🎬 Reel saved to: {output}")


# --- Main Runner ---
if __name__ == "__main__":
    TICKER = "^NSEI"
    START_DATE = "2020-01-01"
    END_DATE = "2025-07-01"
    FREQ = "M"
    LUMP_SUM = 100000
    

    print("📥 Fetching data...")
    df = fetch_data(TICKER, start=START_DATE, end=END_DATE, freq=FREQ)
    SIP = LUMP_SUM/len(df)  # Monthly SIP amount based on total lump sum
    df = calculate_investments(df, lump_sum_amt=LUMP_SUM, sip_amt=SIP)

    stock_name = get_stock_info(TICKER)
    start_year = df.index[0].year

    print(f"📊 Company: {stock_name}")

    print("🎨 Generating frames...")
    generate_frames(df, stock_name=stock_name, ticker=TICKER, start_year=start_year)

    print("🎞 Creating video...")
    create_video()

    print("✅ Done! Your Instagram Reel is ready.")
