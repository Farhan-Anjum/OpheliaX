import streamlit as st


import sys
sys.path.append("C:/Users/Farhan Anjum/Desktop/OpheliaX/Frontend")

from components.sidebar import render_sidebar
from components.trends import render_trend_analysis
from components.chat import render_chat_interface
from auth.google_auth import google_login

def main():
    st.set_page_config(
        page_title="Ophelia Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    # Authentication
    user = google_login()
    if not user:
        st.warning("Please login to continue")
        return
    
    # Main layout
    render_sidebar()
    
    # Tabs
    tab1, tab2 = st.tabs(["Trend Analysis", "Chat"])
    
    with tab1:
        render_trend_analysis()
    
    with tab2:
        render_chat_interface()

if __name__ == "__main__":
    main()