import streamlit as st
import sys
sys.path.append("C:/Users/Farhan Anjum/Desktop/OpheliaX/Frontend")

from components.sidebar import render_sidebar
from components.trends import render_trend_analysis
from components.chat import render_chat_interface
from auth.google_auth import create_flow, get_user_info

def main():
    st.set_page_config(
        page_title="Ophelia Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state for credentials and user_info
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None
    
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    # Authentication
    if not st.session_state.credentials:
        # Create OAuth flow
        flow = create_flow()
        
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        st.write("Please login with Google to continue")
        
        # Create login button
        if st.button("Login with Google"):
            st.markdown(f'<a href="{auth_url}" target="_self">Click here to login</a>', 
                       unsafe_allow_html=True)
        
        # Handle OAuth callback
        query_params = st.experimental_get_query_params()
        if 'code' in query_params:
            try:
                flow = create_flow()
                flow.fetch_token(code=query_params['code'][0])
                st.session_state.credentials = flow.credentials
                
                # Get user info
                user_info = get_user_info(flow.credentials)
                if user_info:
                    st.session_state.user_info = user_info
                    st.experimental_rerun()
                
            except Exception as e:
                st.error(f"Error during authentication: {str(e)}")
    
    else:
        # User is authenticated, display user info
        user = st.session_state.user_info
        st.sidebar.write(f"Welcome {user.get('name')}!")
        if 'picture' in user:
            st.sidebar.image(user['picture'], width=100)
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.credentials = None
            st.session_state.user_info = None
            st.experimental_rerun()

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