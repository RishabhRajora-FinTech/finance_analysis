from plotter import PlotBuilderOneDay
from simulator import InvestmentSimulator
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import os
import shutil
from moviepy import ImageSequenceClip
from concurrent.futures import ProcessPoolExecutor
from functools import partial



def save_financial_summary(file_name, currency, final_value, total_invested, cagr, returns, stock_name, desc):

    def format_dict_content(d):
        return '\n'.join(f"{k}: {v}" for k, v in d.items())

    percentage_return = (returns / total_invested) * 100
    desc_str = format_dict_content(desc) if isinstance(desc, dict) else desc
    content = (
        f"📈 Final Value: {currency} {final_value:,.2f}\n"
        f"💰 Total Invested: {currency} {total_invested:,.2f}\n"
        f"📊 CAGR: {cagr:.2%}\n"
        f"📉 Total Returns: {currency} {returns:,.2f}\n"
        f"📈 Percentage Return: {percentage_return:.2f}%\n"
        f"📊 Company: {stock_name}\n\n"
        f"ℹ️ Description: {desc_str}\n\n"
        f"Data Source: Yahoo Finance\n"
        f"Don't Wait, start investing today!\n"
        f"Follow us for more stock price animations\n"
        f"⚠️ Disclaimer: For informational and entertainment pusposes only. Not Financial advice. Past Performance is no guarantee of future results.\n"
    )
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"✅ Summary saved to {file_name}")


def generate_single_frame(df: pd.DataFrame, idx: int, frame_num: int, folder: str, ticker: str, stock_name: str, start_year: int, daily_investment: float, currency: str):
    df_clip = df.iloc[:idx].copy()
    plot = PlotBuilderOneDay(df_clip, ticker=ticker, start_year=start_year, name=stock_name, daily_investment=daily_investment, currency=currency)
    fig = plot.create_plot()
    fig.update_layout(width=1080, height=1920)
    frame_path = os.path.join(folder, f"frame_{frame_num:03d}.png")
    fig.write_image(frame_path, width=1080, height=1920, scale=1)
    print(f"✅ Saved: {frame_path}")
    return frame_path

def generate_frames_parallel(
    df: pd.DataFrame,
    stock_name: str,
    ticker: str,
    start_year: int,
    folder: str = "frames",
    num_frames: int = 200,
    daily_investment: float = 1.0,
    currency: str = "USD",
    max_workers: int = os.cpu_count()
):
    # 1. Clean and create folder
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    n = len(df)
    if n >= num_frames:
        cut_points = np.linspace(1, n, num=num_frames, dtype=int, endpoint=True)
    else:
        cut_points = np.arange(1, n + 1, dtype=int)
        pad = np.full(num_frames - n, n, dtype=int)
        cut_points = np.concatenate([cut_points, pad])

    # 2. Prepare partial function for multiprocessing
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        tasks = [
            executor.submit(
                generate_single_frame, df, idx, frame_num, folder, ticker, stock_name, start_year, daily_investment, currency
            )
            for frame_num, idx in enumerate(cut_points, start=1)
        ]
        for task in tasks:
            task.result()  # To ensure exceptions are caught

    print(f"\n🎉 Generated {len(cut_points)} frames in '{folder}'")

def generate_frames(
    df: pd.DataFrame,
    stock_name: str,
    ticker: str,
    start_year: int,
    folder: str = "frames",
    num_frames: int = 200,
    daily_investment: float = 1.0,
    currency: str = "USD"
):
    # 1. Clean output folder
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    n = len(df)
    # 2. Decide which slice endpoints to use
    if n >= num_frames:
        # even‐spaced cuts from 1…n
        cut_points = np.linspace(1, n, num=num_frames, dtype=int, endpoint=True)
    else:
        # fewer rows than frames: use every row, then duplicate last
        cut_points = np.arange(1, n + 1, dtype=int)
        # pad with the final index to reach exactly num_frames
        pad = np.full(num_frames - n, n, dtype=int)
        cut_points = np.concatenate([cut_points, pad])

    # 3. Generate one image per cut point
    for frame_num, idx in enumerate(cut_points, start=1):
        df_clip = df.iloc[:idx].copy()
        plot = PlotBuilderOneDay(df_clip, ticker=ticker, start_year=start_year, name=stock_name,daily_investment=daily_investment, currency=currency)
        fig = plot.create_plot()

        # Ensure reel dimensions
        fig.update_layout(width=1080, height=1920)

        frame_path = os.path.join(folder, f"frame_{frame_num:03d}.png")
        fig.write_image(frame_path, width=1080, height=1920, scale=1)
        print(f"✅ Saved: {frame_path}")

    print(f"\n🎉 Generated {len(cut_points)} frames in '{folder}'")

# --- Compile Frames into MP4 Reel ---
def create_video(folder='frames', output='investment_growth_reel.mp4', fps=10):
    frames = sorted([f"{folder}/{f}" for f in os.listdir(folder) if f.endswith(".png")])
    clip = ImageSequenceClip(frames, fps=fps)
    # clip = clip.fx(resize, (1080, 1920))  # Ensure 9:16 size
    clip.write_videofile(output, codec='libx264', audio=False)
    print(f"🎬 Reel saved to: {output}")

#

if __name__ == "__main__":
    TICKER = "M&M.NS"
    start_year = 2005
    ticker = TICKER
    daily_investment = 100.0  # Daily investment amount
    currency = "INR"  # Currency for the investment
    simulator = InvestmentSimulator(ticker, start_year, daily_investment=daily_investment)
    simulator.simulate()
    final_value, total_invested, cagr, df, desc = simulator.get_results()
    stock_name = simulator.get_stock_info()

    print('Description',desc)

    print(df.head(15))

    # plotter = PlotBuilderOneDay(df, ticker, start_year, stock_name)   

    # fig = plotter.create_plot()
    # Metrics
    # Display results in terminal (or can be adapted for GUI)
    returns = final_value - total_invested
    print(f"📈 Final Value: {currency} {final_value:,.2f}")
    print(f"💰 Total Invested:  {currency}{total_invested:,.2f}")
    print(f"📊 CAGR:  {cagr:.2%}")
    print(f"📉 Total Returns:  {currency} {returns:,.2f}")
    percentage_return = (returns / total_invested) * 100
    print(f"📈 Percentage Return: {percentage_return:.2f}%")
    
    print(f"📊 Company: {stock_name}")
    save_financial_summary(f"summary{TICKER}.txt", f"{currency}", final_value, total_invested, cagr, returns, stock_name, desc)


    print("🎨 Generating frames...")
    generate_frames_parallel(df, stock_name=stock_name, ticker=TICKER, start_year=start_year, daily_investment=daily_investment, currency=currency)

    print("🎞 Creating video...")
    create_video()

    print("✅ Done! Your Instagram Reel is ready.")
