import streamlit as st

def app():
    st.title("🏠 Welcome to the Share Price Tracker")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Lump Sum & SIP", key="btn_lump"):
            st.session_state.current_page = "Lump Sum & SIP"
            st.experimental_rerun()

        if st.button("📊 Portfolio Analysis", key="btn_portfolio"):
            st.session_state.current_page = "Portfolio Analysis"
            st.experimental_rerun()

    with col2:
        if st.button("ℹ️ About", key="btn_about"):
            st.session_state.current_page = "About"
            st.experimental_rerun()
