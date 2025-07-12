import plotly.graph_objects as go
from io import BytesIO
import pandas as pd

class PlotBuilder:
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
            title=f" ₹1/day in {self.tikcer_name} ticker {self.ticker} since {start_date.strftime("%d/%m/%Y")} (AVAL. DATA) input {self.start_year}",
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
