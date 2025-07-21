import plotly.graph_objects as go
import numpy as np

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
