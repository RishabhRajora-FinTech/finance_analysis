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
    

class PlotBuilderOneDay:
    def __init__(self, df: pd.DataFrame, ticker: str, start_year: int, name: str = None):
        self.df = df
        self.ticker = ticker
        self.start_year = start_year
        self.tikcer_name = name

    def create_plot(self):
        fig = go.Figure()

        # Add Portfolio Value Line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['Portfolio Value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='green')
        ))

        # Add Total Invested Line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['Total Invested'],
            mode='lines',
            name='Total Invested',
            line=dict(color='red')
        ))

        # Final values for annotations
        start_date = self.df.index[0]
        final_date = self.df.index[-1]
        final_portfolio = self.df['Portfolio Value'].iloc[-1]
        final_invested = self.df['Total Invested'].iloc[-1]

        # Annotate Portfolio Value
        fig.add_annotation(
            x=final_date,
            y=final_portfolio,
            text=f"₹{final_portfolio:,.0f}",
            showarrow=True,
            arrowhead=1,
            ax=-80,
            ay=-40,
            font=dict(color='green')
        )

        # Annotate Total Invested
        fig.add_annotation(

            x=self.df.index[-1],
            y=final_portfolio,
            text=f"<b>₹{final_portfolio:,.0f}</b>",
            showarrow=True,
            arrowhead=2,
            ax=-80,
            ay=-40,
            font=dict(color="white"),
            align="center",
            bordercolor="green",
            borderwidth=2,
            borderpad=4,
            bgcolor="green",
            opacity=0.9
        )

        fig.add_annotation(
            x=self.df.index[-1],
            y=final_invested,
            text=f"<b>₹{final_invested:,.0f}</b>",
            showarrow=True,
            arrowhead=2,
            ax=-80,
            ay=40,
            font=dict(color="white"),
            align="center",
            bordercolor="red",
            borderwidth=2,
            borderpad=4,
            bgcolor="red",
            opacity=0.9
        )



        # Layout styling
        fig.update_layout(
            title=f" ₹1/day in {self.tikcer_name} ticker {self.ticker} since {start_date.strftime("%d/%m/%Y")} (AVAL. DATA) range from {self.start_year} & Investment Duration {len(self.df.index)} days",
            xaxis=dict(
                title="Date",
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title=dict(
                    text="INR",
                    font=dict(size=14)
                ),
                tickfont=dict(size=12)
            ),
            autosize=False,
            width=800,
            height=500,
            margin=dict(l=50, r=50, b=100, t=100, pad=5),
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font=dict(color='white'),
            legend=dict(x=0, y=1.1, orientation="h")
        )


        return fig

    def get_image_bytes(self):
        fig = self.create_plot()
        buf = BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)
        return buf

