import streamlit as st
from simulator import InvestmentSimulator
from plotter import PlotBuilder

st.set_page_config(page_title="📈  ₹1/day Investment", layout="centered")
st.title("💵 ₹ 1 a Day Investment Simulator")

# Sidebar Inputs
st.sidebar.markdown("**Everything FinTech**", unsafe_allow_html=True)
st.sidebar.markdown("**Created by ❤️ Rishabh Rajora**", unsafe_allow_html=True)

st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker Symbol", value="^NSEI", help="Enter the stock ticker symbol (e.g., 'NSE:IDEA' or 'NASDAQ:AAPL').")
start_year = st.sidebar.slider("Start Year", min_value=1990, max_value=2025, value=1995)


# Run Simulation
simulator = InvestmentSimulator(ticker, start_year)
simulator.simulate()
final_value, total_invested, cagr, df = simulator.get_results()
name = simulator.get_stock_info()

# Metrics
st.metric("Name", name)
st.metric("Total Invested", f"₹{total_invested:,.0f}")
st.metric("Portfolio Value", f"₹{final_value:,.0f}")
st.metric("Annualized Return (CAGR)", f"{cagr:.2f}%")
st.metric("Investment Duration", f"{len(df.index)} days")

# Plot (using Plotly)
plotter = PlotBuilder(df, ticker, start_year, name)
fig = plotter.create_plot()
st.plotly_chart(fig, use_container_width=True)

# # Download (still works via PNG with Plotly)
# st.download_button("📥 Download Chart", data=plotter.get_image_bytes(),
#                    file_name="investment_chart.png", mime="image/png")

st.download_button(
    "📥 Download Interactive Chart (HTML)",
    data=fig.to_html(),
    file_name="chart.html",
    mime="text/html"
)

st.markdown("---")
st.caption("Built with Python OOP & Streamlit 🐍")
