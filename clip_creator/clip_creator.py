import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import os
import shutil
from moviepy import ImageSequenceClip


# --- Step 1: Fetch stock data ---
def fetch_data(ticker, start="2024-01-01", end="2024-01-31", freq='W'):
    df = yf.download(ticker, start=start, end=end)[['Close']]
    df = df.resample(freq).first().dropna()

    if isinstance(df.index, pd.PeriodIndex):
        df.index = df.index.to_timestamp()
    else:
        df.index = pd.to_datetime(df.index)

    return df


# --- Step 2: Calculate Lump Sum and SIP portfolio values ---
def calculate_investments(df, lump_sum_amt=10000, sip_amt=500):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df['Shares_Lump'] = lump_sum_amt / df.iloc[0]['Close']
    df['Value_Lump'] = df['Shares_Lump'] * df['Close']
    df['Shares_SIP'] = (sip_amt / df['Close']).cumsum()
    df['Value_SIP'] = df['Shares_SIP'] * df['Close']
    df.index = pd.to_datetime(df.index)
    df['Formatted_Date'] = df.index.strftime('%d-%m-%Y')  # Force string format for clean x-axis

    return df


# --- Step 3: Generate Instagram Reel-sized frames ---
def generate_frames(df, folder='frames'):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    for i in range(1, len(df) + 1):
        fig = go.Figure()

        # Plot Lump Sum
        fig.add_trace(go.Scatter(
            x=df['Formatted_Date'][:i],
            y=df['Value_Lump'][:i],
            mode='lines+markers',
            name='Lump Sum',
            line=dict(width=4)
        ))

        # Plot SIP
        fig.add_trace(go.Scatter(
            x=df['Formatted_Date'][:i],
            y=df['Value_SIP'][:i],
            mode='lines+markers',
            name='SIP',
            line=dict(width=4)
        ))

        # Add date annotation
        annotation_date = df['Formatted_Date'].iloc[i - 1]
        fig.add_annotation(
            text=f"Date: {annotation_date}",
            xref="paper", yref="paper",
            x=0.95, y=1.05,
            showarrow=False,
            font=dict(size=24),
            align="right"
        )

        # Layout: 9:16 vertical for Instagram Reels
        fig.update_layout(
            width=1080,
            height=1920,
            template='plotly_dark',
            margin=dict(t=120, b=100, l=40, r=40),
            title=dict(
                text="📊 Lump Sum vs SIP Portfolio",
                x=0.5,
                xanchor='center',
                font=dict(size=36)
            ),
            font=dict(size=22),
            xaxis_title="Date",
            yaxis_title="Portfolio Value (₹)",
            legend=dict(
                orientation='h',
                x=0.5,
                y=-0.2,
                xanchor='center',
                font=dict(size=22)
            )
        )

        # Use category axis to keep dd-mm-yyyy string labels clean
        fig.update_xaxes(
            type="category",
            tickangle=-45,
            title_text="Date"
        )

        # Save each frame
        frame_path = f"{folder}/frame_{i:03d}.png"
        fig.write_image(frame_path)
        print(f"✅ Saved: {frame_path}")


# --- Step 4: Combine frames into vertical video ---
def create_video(folder='frames', output='investment_growth_reel.mp4', fps=10):
    frames = sorted([f"{folder}/{f}" for f in os.listdir(folder) if f.endswith(".png")])
    clip = ImageSequenceClip(frames, fps=fps)
    # clip = clip.resize((1080, 1920))  # 💡 Ensure 9:16 portrait format
    clip.write_videofile(output, codec='libx264', audio=False)
    print(f"🎬 Reel saved to: {output}")


# --- Main execution ---
if __name__ == "__main__":
    TICKER = "INFY.NS"  # Change as needed
    FREQ = "W"          # 'D', 'W', or 'M'
    LUMP_SUM = 10000
    SIP = 500

    print("📥 Fetching data...")
    df = fetch_data(TICKER, freq=FREQ)
    df = calculate_investments(df, lump_sum_amt=LUMP_SUM, sip_amt=SIP)

    print("🎨 Generating frames...")
    generate_frames(df)

    print("🎞 Creating video...")
    create_video()

    print("✅ Done! Upload the reel to Instagram.")
