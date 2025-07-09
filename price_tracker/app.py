import streamlit as st
from app_pages import home, lumsump_sip, portfolio_analysis, about

# Set layout before anything else
st.set_page_config(page_title="📈 Share Tracker", layout="wide")

# Routing using session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Optional: Sidebar widgets (you can add filters or tickers here)
with st.sidebar:
#     st.title("🔍 Portfolio Builder")
#     st.selectbox("Search tickers", options=["TCS.NS", "INFY.NS", "AAPL"])
#     st.date_input("Start Date", key="start_date")
#     st.date_input("End Date", key="end_date")
    st.markdown("---")
    if st.button("🏠 Home", key="sidebar_home"):
        st.session_state.current_page = "Home"
    if st.button("📈 Lump Sum & SIP", key="sidebar_lump"):
        st.session_state.current_page = "Lump Sum & SIP"
    if st.button("📊 Portfolio Analysis", key="sidebar_portfolio"):
        st.session_state.current_page = "Portfolio Analysis"
    if st.button("ℹ️ About", key="sidebar_about"):
        st.session_state.current_page = "About"
# Render the selected page
PAGES = {
    "Home": home,
    "Lump Sum & SIP": lumsump_sip,
    "Portfolio Analysis": portfolio_analysis,
    "About": about,
}

PAGES[st.session_state.current_page].app()
