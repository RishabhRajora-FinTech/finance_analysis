import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import pandas as pd

class PlotBuilder:
    def __init__(self, df, ticker, start_year, name=""):
        self.df = df.copy()
        self.ticker = ticker
        self.start_year = start_year
        self.name = name or ticker
        self.df['Formatted_Date'] = self.df.index.strftime('%d-%m-%Y')

    def create_plot(self):
        fig = go.Figure()

        # Add SIP trace
        fig.add_trace(go.Scatter(
            x=self.df['Formatted_Date'],
            y=self.df['Value_SIP'],
            mode='lines+markers',
            name='SIP Investment',
            line=dict(color='dodgerblue', width=4)
        ))

        # Add Lump Sum trace
        fig.add_trace(go.Scatter(
            x=self.df['Formatted_Date'],
            y=self.df['Value_Lump'],
            mode='lines+markers',
            name='Lump Sum Investment',
            line=dict(color='tomato', width=4, dash='dot')
        ))

        # Final value annotations
        if len(self.df) > 0:
            final_date = self.df['Formatted_Date'].iloc[-1]
            sip_val = self.df['Value_SIP'].iloc[-1]
            lump_val = self.df['Value_Lump'].iloc[-1]

            fig.add_annotation(
                text=f"SIP: ₹{sip_val:,.0f}",
                x=final_date, y=sip_val,
                showarrow=True,
                arrowhead=1,
                font=dict(size=36, color="dodgerblue"),
                ax=0, ay=-40
            )

            fig.add_annotation(
                text=f"Lump Sum: ₹{lump_val:,.0f}",
                x=final_date, y=lump_val,
                showarrow=True,
                arrowhead=1,
                font=dict(size=36, color="tomato"),
                ax=0, ay=40
            )

        # Determine spacing of x-ticks
        total_points = len(self.df)
        tick_every = max(1, total_points // 6)  # Show max 6 labels
        tickvals = self.df['Formatted_Date'].iloc[::tick_every].tolist()

        # Layout
        fig.update_layout(
            width=1080,  # ✅ Instagram Reel width
            height=1920,  # ✅ Instagram Reel height
            title=dict(
                text=f"📊 {self.name}<br>Lump Sum vs SIP",
                x=0.1, xanchor='left',
                font=dict(size=36)  # Enlarged for portrait
            ),
            xaxis_title="Date",
            yaxis_title="Portfolio Value (₹)",
            font=dict(size=24),
            template="plotly_dark",
            legend=dict(
                orientation='h',
                x=0.5,
                y=-0.2,
                xanchor='center',
                font=dict(size=20)
            ),
            margin=dict(t=120, b=100, l=60, r=60)
        )

        fig.update_xaxes(
            type="category",
            tickangle=-45,
            tickvals=tickvals,
            ticktext=tickvals
        )

        return fig
    
import os
import shutil
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import shutil
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.graph_objects as go


class PlotBuilderOneDay:
    REQUIRED_COLS = ("Portfolio Value", "Total Invested")

    def __init__(self, df: pd.DataFrame, ticker: str, start_year: int, name: str = None):
        self.df = df.copy()
        self.ticker = ticker
        self.start_year = start_year
        self.ticker_name = name or ticker

        # ---- sanity checks ----
        missing = [c for c in self.REQUIRED_COLS if c not in self.df.columns]
        if missing:
            raise ValueError(f"DataFrame is missing required columns: {missing}")

        # ---- ensure datetime index ----
        self._ensure_datetime_index()

        # ---- clean & order ----
        self.df.sort_index(inplace=True)
        self.df = self.df.dropna(subset=list(self.REQUIRED_COLS))

        # ---- add a human‐readable date column ----
        self.df['Formatted_Date'] = self.df.index.strftime('%d-%m-%Y')

    def _ensure_datetime_index(self):
        """Make df.index a datetime index, inferring from ints if needed."""
        idx = self.df.index
        if pd.api.types.is_datetime64_any_dtype(idx):
            return
        if pd.api.types.is_integer_dtype(idx):
            max_v = int(np.max(idx))
            unit = (
                "ns" if max_v > 1e17 else
                "us" if max_v > 1e14 else
                "ms" if max_v > 1e12 else
                "s"
            )
            self.df.index = pd.to_datetime(idx, unit=unit)
        else:
            self.df.index = pd.to_datetime(idx)

    def create_plot(self) -> go.Figure:
        fig = go.Figure()
        draw_mode = "lines+markers"

        # Portfolio Value line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df["Portfolio Value"],
            customdata=self.df["Formatted_Date"],
            mode=draw_mode,
            name="Portfolio Value",
            line=dict(color="green", width=4),
            marker=dict(size=8),
            connectgaps=True,
            hovertemplate="%{customdata}<br>₹%{y:,.0f}<extra>Portfolio Value</extra>",
        ))

        # Total Invested line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df["Total Invested"],
            customdata=self.df["Formatted_Date"],
            mode=draw_mode,
            name="Total Invested",
            line=dict(color="red", width=4, dash="dot"),
            marker=dict(size=8),
            connectgaps=True,
            hovertemplate="%{customdata}<br>₹%{y:,.0f}<extra>Total Invested</extra>",
        ))
        # ─── lock & relabel the x-axis ─────────────────────────────────────
            # First ensure 'Formatted_Date' exists and is correctly formatted
        if "Formatted_Date" not in self.df.columns:
            self.df["Formatted_Date"] = self.df.index.strftime("%d-%m-%Y")

        # Limit number of ticks to avoid clutter (especially on 1080px wide plots)
        max_ticks = 10
        step = max(1, len(self.df) // max_ticks)
        tickvals = self.df.index[::step]
        ticktext = self.df["Formatted_Date"].iloc[::step]

        # Apply to x-axis
        fig.update_xaxes(
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle=45,
            title="Date",
            showgrid=True,
            tickfont=dict(size=12)
        )
        # PIN Y-AXIS JUST ABOVE MAX
        ymax = self.df["Portfolio Value"].max() * 1.1
        fig.update_yaxes(
            range=[0, ymax],
            title="INR",
            showgrid=True,
            tickfont=dict(size=12),
        )

        # ANNOTATE LAST POINT USING Formatted_Date
        final_date_disp = self.df["Formatted_Date"].iloc[-1]
        final_portfolio = float(self.df["Portfolio Value"].iloc[-1])
        final_invested = float(self.df["Total Invested"].iloc[-1])

        fig.add_annotation(
            x=self.df.index[-1], y=final_portfolio,
            text=f"{final_date_disp}<br><b>₹{final_portfolio:,.0f}</b>",
            showarrow=True, arrowhead=2, ax=-70, ay=-40,
            font=dict(color="white",size = 20), align="center",
            bordercolor="green", borderwidth=3, borderpad=8,
            bgcolor="green", opacity=0.95,
        )
        fig.add_annotation(
            x=self.df.index[-1], y=final_invested,
            text=f"{final_date_disp}<br><b>₹{final_invested:,.0f}</b>",
            showarrow=True, arrowhead=2, ax=-70, ay=40,
            font=dict(color="white",size = 20), align="center",
            
            bordercolor="red", borderwidth=3, borderpad=8,
            bgcolor="red", opacity=0.95,
        )

        # FINAL LAYOUT
        start_date_str = self.df["Formatted_Date"].iloc[0]
        fig.update_layout(
            title=(
                f"₹100/day in {self.ticker_name} ({self.ticker}) since {start_date_str} "
                f"(DATA from {self.start_year}) • Duration: {len(self.df)} days"
            ),
            autosize=False, width=1080, height=1920,
            margin=dict(l=50, r=50, b=120, t=120, pad=5),
            # paper_bgcolor="#2c3548", plot_bgcolor="#c1c9d9",
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_gridcolor='lightgrey',
            yaxis_gridcolor='lightgrey',
            font=dict(color="black"), legend=dict(x=0, y=1.1, orientation="h"),
        )

        return fig

    def get_image_bytes(self, fmt: str = "png") -> BytesIO:
        fig = self.create_plot()
        buf = BytesIO()
        fig.write_image(buf, format=fmt)
        buf.seek(0)
        return buf


def generate_frames(
    df: pd.DataFrame,
    stock_name: str,
    ticker: str,
    start_year: int,
    folder: str = "frames",
    num_frames: int = 100,
):
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

    for frame_num, idx in enumerate(cut_points, start=1):
        df_clip = df.iloc[:idx].copy()
        plot = PlotBuilderOneDay(df_clip, ticker=ticker, start_year=start_year, name=stock_name)
        fig = plot.create_plot()
        fig.update_layout(width=1080, height=1920)

        frame_path = os.path.join(folder, f"frame_{frame_num:03d}.png")
        fig.write_image(frame_path, width=1080, height=1920, scale=1)
        print(f"✅ Saved: {frame_path}")

    print(f"\n🎉 Generated {num_frames} frames in '{folder}'")
