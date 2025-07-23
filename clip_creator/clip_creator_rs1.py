from plotter import PlotBuilderOneDay
from simulator import InvestmentSimulator
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import os
import shutil
from moviepy import ImageSequenceClip

# --- Generate Frames using PlotBuilder ---
def generate_frames(df, stock_name, ticker, start_year, folder='frames'):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    for i in range(1, len(df) + 1):
        df_clip = df.iloc[:i].copy()

        # 🔁 Use PlotBuilder to generate annotated Reel plot
        plot = PlotBuilderOneDay(df_clip, ticker=ticker, start_year=start_year, name=stock_name)
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

#

if __name__ == "__main__":
    TICKER = "IDEA.NS"
    start_year = 2010
    ticker = TICKER
    simulator = InvestmentSimulator(ticker, start_year)
    simulator.simulate()
    final_value, total_invested, cagr, df = simulator.get_results()
    stock_name = simulator.get_stock_info()

    plotter = PlotBuilderOneDay(df, ticker, start_year, stock_name)   

    fig = plotter.create_plot()
    # Metrics
    # Display results in terminal (or can be adapted for GUI)
    
    print(f"📊 Company: {stock_name}")

    print("🎨 Generating frames...")
    generate_frames(df, stock_name=stock_name, ticker=TICKER, start_year=start_year)

    print("🎞 Creating video...")
    create_video()

    print("✅ Done! Your Instagram Reel is ready.")
