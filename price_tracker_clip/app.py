import streamlit as st
from simulator import InvestmentSimulator
from plotter import PlotBuilder

st.set_page_config(page_title="📈 $1/day Investment", layout="centered")
st.title("💵 $1 a Day Investment Simulator")

# Sidebar Inputs
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Ticker Symbol", value="ROST")
start_year = st.sidebar.slider("Start Year", min_value=1980, max_value=2023, value=1985)

# Run Simulation
simulator = InvestmentSimulator(ticker, start_year)
simulator.simulate()
final_value, total_invested, cagr, df = simulator.get_results()

# Metrics
st.metric("Total Invested", f"${total_invested:,.0f}")
st.metric("Portfolio Value", f"${final_value:,.0f}")
st.metric("Annualized Return (CAGR)", f"{cagr:.2f}%")

# Plot
plotter = PlotBuilder(df, ticker, start_year)
fig = plotter.create_plot()
st.pyplot(fig)

# Download
st.download_button("📥 Download Chart", data=plotter.get_image_bytes(),
                   file_name="investment_chart.png", mime="image/png")

st.markdown("---")
st.caption("Built with Python OOP & Streamlit 🐍")
