import matplotlib.pyplot as plt
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import pandas as pd
import tempfile
import os

def generate_investment_video(df, ticker="ROST", start_year=1985, duration=8):
    df = df.reset_index()
    frames = len(df)

    fig, ax = plt.subplots(figsize=(8, 6))

    def make_frame(t):
        i = int((t / duration) * frames)
        i = min(i, frames - 1)
        ax.clear()

        ax.plot(df['Date'][:i+1], df['Portfolio Value'][:i+1], color='green', label='Portfolio Value')
        ax.plot(df['Date'][:i+1], df['Total Invested'][:i+1], color='red', label='Total Invested')
        ax.set_title(f"$1/day in {ticker} since {start_year}", fontsize=14)
        ax.set_xlabel("Date")
        ax.set_ylabel("USD")
        ax.grid(True)
        ax.legend()

        if i == frames - 1:
            ax.text(df['Date'][i], df['Portfolio Value'][i], f"${df['Portfolio Value'][i]:,.0f}", color='green', fontsize=12)
            ax.text(df['Date'][i], df['Total Invested'][i], f"${df['Total Invested'][i]:,.0f}", color='red', fontsize=12)

        return mplfig_to_npimage(fig)

    animated_clip = VideoClip(make_frame, duration=duration).set_fps(24)

    # Add overlay title
    title = TextClip(f"$1/day in {ticker} since {start_year}",
                     fontsize=40, color='white', font='Arial-Bold', bg_color='black').set_duration(duration)
    title = title.set_position(("center", "top"))

    final_clip = CompositeVideoClip([animated_clip, title])

    # Save to temp file
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, f"{ticker}_investment.mp4")
    final_clip.write_videofile(video_path, fps=24, codec='libx264', audio=False, verbose=False, logger=None)

    return video_path
