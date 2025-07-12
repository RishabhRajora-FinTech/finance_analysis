import matplotlib.pyplot as plt
from io import BytesIO

class PlotBuilder:
    def __init__(self, df, ticker: str, start_year: int):
        self.df = df
        self.ticker = ticker
        self.start_year = start_year

    def create_plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.df.index, self.df['Portfolio Value'], label='Portfolio Value', color='green')
        ax.plot(self.df.index, self.df['Total Invested'], label='Total Invested', color='red')

        ax.set_title(f"$1/day in {self.ticker} since {self.start_year}", fontsize=16)
        ax.set_ylabel("USD")
        ax.grid(True)
        ax.legend()

        # Annotations
        final_value = self.df['Portfolio Value'].iloc[-1]
        total_invested = self.df['Total Invested'].iloc[-1]

        ax.annotate(f"${final_value:,.0f}", xy=(self.df.index[-1], final_value), xytext=(-100, 10),
                    textcoords='offset points', arrowprops=dict(arrowstyle="->"), fontsize=10, color='green')
        ax.annotate(f"${total_invested:,.0f}", xy=(self.df.index[-1], total_invested), xytext=(-100, -20),
                    textcoords='offset points', arrowprops=dict(arrowstyle="->"), fontsize=10, color='red')

        return fig

    def get_image_bytes(self):
        fig = self.create_plot()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return buf
