import plotly.graph_objects as go

class PlotBuilder:
    def __init__(self, df, ticker, start_year, name=""):
        self.df = df.copy()
        self.ticker = ticker
        self.start_year = start_year
        self.name = name or ticker

        # Format x-axis labels as string
        self.df['Formatted_Date'] = self.df.index.strftime('%d-%m-%Y')

    def create_plot(self):
        fig = go.Figure()

        # --- SIP Plot ---
        fig.add_trace(go.Scatter(
            x=self.df['Formatted_Date'],
            y=self.df['Value_SIP'],
            mode='lines+markers',
            name='SIP Investment',
            line=dict(color='dodgerblue', width=4)
        ))

        # --- Lump Sum Plot ---
        fig.add_trace(go.Scatter(
            x=self.df['Formatted_Date'],
            y=self.df['Value_Lump'],
            mode='lines+markers',
            name='Lump Sum Investment',
            line=dict(color='tomato', width=4, dash='dot')
        ))

        # --- Final Value Annotations ---
        if len(self.df) > 0:
            final_date = self.df['Formatted_Date'].iloc[-1]
            sip_val = self.df['Value_SIP'].iloc[-1]
            lump_val = self.df['Value_Lump'].iloc[-1]

            fig.add_annotation(
                text=f"SIP: ₹{sip_val:,.0f}",
                x=final_date, y=sip_val,
                showarrow=True, arrowhead=1,
                font=dict(size=18, color="dodgerblue"),
                ax=0, ay=-40
            )

            fig.add_annotation(
                text=f"Lump Sum: ₹{lump_val:,.0f}",
                x=final_date, y=lump_val,
                showarrow=True, arrowhead=1,
                font=dict(size=18, color="tomato"),
                ax=0, ay=40
            )

        # --- Layout & Axis ---
        fig.update_layout(
            title=dict(
                text=f"📊 {self.name}<br>Lump Sum vs SIP",
                x=0.5, xanchor='center',
                font=dict(size=36)
            ),
            xaxis_title="Date",
            yaxis_title="Portfolio Value (₹)",
            font=dict(size=22),
            template="plotly_dark",
            legend=dict(
                orientation='h',
                x=0.5, y=-0.2,
                xanchor='center'
            ),
            margin=dict(t=120, b=100, l=40, r=40)
        )

        fig.update_xaxes(
            type="category",
            tickangle=-45,
            tickvals=self.df['Formatted_Date'],
            ticktext=self.df['Formatted_Date']
        )

        return fig
