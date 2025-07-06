import streamlit as st
from utils import get_stock_data, simulate_lumpsum, simulate_sip, get_stock_info
import plotly.graph_objects as go
from datetime import date
import pandas as pd

from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="📈 Share Price Tracker", layout="wide")

st.title("📈 Share Price Investment Tracker (Lump Sum vs SIP)")

# --- User Inputs ---
ticker = st.text_input("Enter Stock Symbol (e.g., TCS.NS, INFY.NS, AAPL)", "TCS.NS")
st.write("Name of the Company:",get_stock_info(ticker))
start_date = st.date_input("Start Date", date(2015, 1, 1))
end_date = st.date_input("End Date", date.today())

invest_type = st.selectbox("Investment Type", ["Lump Sum", "SIP"])
amount = st.number_input(
    "Investment Amount (INR/USD)",
    min_value=100.0,
    value=100000.0 if invest_type == "Lump Sum" else 5000.0
)
# Calculate duration in months and years
if start_date and end_date:
    duration = relativedelta(end_date, start_date)
    duration_months = duration.months + duration.years * 12
    st.write(f"Duration: {duration.years} years and {duration.months} months ({duration_months} months total)")

# --- Main Logic ---
if st.button("Track"):
    data = get_stock_data(ticker, start_date, end_date)

    if data.empty:
        st.error("❌ No data found for the given ticker or date range.")
    else:
        # --- Price Chart with Moving Average ---
        # --- Updated Price History Chart with 30/90 MA ---
        # --- Clean & Working Price Chart Block ---
        st.subheader(f"📊 {ticker.upper()} Price History")

        # Fetch clean price data and drop NaNs
        price_series = data.dropna()

        # Ensure it's a pandas Series (not a DataFrame column mistakenly wrapped)
        if isinstance(price_series, pd.DataFrame):
            price_series = price_series.iloc[:, 0]

        # Calculate moving averages
        ma30 = price_series.rolling(30).mean()
        ma90 = price_series.rolling(90).mean()

        # Plotly figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=price_series.index,
            y=price_series.values,
            mode="lines",
            name="Close Price",
            line=dict(width=2, color="royalblue"),
            hovertemplate="Date: %{x}<br>Close: ₹%{y:.2f}<extra></extra>"
        ))

        fig.add_trace(go.Scatter(
            x=ma30.index,
            y=ma30.values,
            mode="lines",
            name="30-Day MA",
            line=dict(dash="dot", color="green"),
            hoverinfo="skip"
        ))

        fig.add_trace(go.Scatter(
            x=ma90.index,
            y=ma90.values,
            mode="lines",
            name="90-Day MA",
            line=dict(dash="dash", color="orange"),
            hoverinfo="skip"
        ))

        fig.update_layout(
            template="plotly_dark",  # ← use dark theme to match your UI
            title=dict(text=f"{ticker.upper()} Closing Price with MAs", x=0.5),
            xaxis_title="Date",
            yaxis_title="Price (₹ or $)",
            hovermode="x unified",
            height=500,
            showlegend=True,
            legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
            margin=dict(l=40, r=40, t=50, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)


        # --- Investment Analysis ---
        if invest_type == "Lump Sum":
            
                        # --- Lump Sum Investment Growth Over Time ---
            shares, final_val, lump_df = simulate_lumpsum(data, amount)
            gain = final_val - amount
            pct_gain = (gain / amount) * 100

            st.success(f"🎯 You bought **{shares:.2f} shares** at ₹{float(data.iloc[0]):.2f}")
            st.info(
                f"💰 Final Value: ₹{final_val:,.2f}\n\n"
                f"💸 Total Invested: ₹{amount:,.2f}\n\n"
                f"📈 Gain: ₹{gain:,.2f} ({pct_gain:.2f}%)"
            )

            st.subheader("📈 Lump Sum Portfolio Value Over Time")

            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=lump_df.index,
                y=lump_df["Invested"],
                mode='lines',
                name='Total Invested',
                line=dict(color="gray", dash="dot")
            ))
            fig3.add_trace(go.Scatter(
                x=lump_df.index,
                y=lump_df["Portfolio Value"],
                mode='lines',
                name='Portfolio Value',
                fill='tonexty',
                line=dict(color="royalblue")
            ))
            fig3.update_layout(
                title="Lump Sum Investment Value Over Time",
                xaxis_title="Date",
                yaxis_title="₹ Value",
                template="plotly_white",
                hovermode="x unified",
                height=450,
                showlegend=True,
                legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
                margin=dict(l=40, r=40, t=50, b=40)
            )
            st.plotly_chart(fig3, use_container_width=True)
            

        else:
            sip_df = simulate_sip(data, amount)
            st.subheader("📈 SIP Investment Growth Over Time")

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=sip_df.index,
                y=sip_df["Invested"],
                mode="lines+markers",
                name="Total Invested",
                fill="tozeroy"
            ))
            fig2.add_trace(go.Scatter(
                x=sip_df.index,
                y=sip_df["Value"],
                mode="lines+markers",
                name="Portfolio Value",
                fill="tonexty"
            ))

            fig2.update_layout(
                height=450,
                xaxis_title="Date",
                yaxis_title="₹ Value",
                template="plotly_white",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig2, use_container_width=True)

            final_val = float(sip_df["Value"].iloc[-1])
            total_inv = float(sip_df["Invested"].iloc[-1])
            gain = final_val - total_inv
            pct_gain = (gain / total_inv) * 100

            st.info(
                f"💰 Final Value: ₹{final_val:,.2f}\n\n"
                f"💸 Total Invested: ₹{total_inv:,.2f}\n\n"
                f"📈 Gain: ₹{gain:,.2f} ({pct_gain:.2f}%)"
            )
