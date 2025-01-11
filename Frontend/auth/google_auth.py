import streamlit as st
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# OAuth 2.0 configuration
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8501'  # Streamlit default port
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

def create_flow():
    """Create OAuth 2.0 flow instance"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    return flow

def get_user_info(credentials):
    """Fetch user information using OAuth2 credentials"""
    try:
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        return user_info
    except Exception as e:
        st.error(f"Error fetching user info: {str(e)}")
        return None

def main():
    st.title("Sign up with Google")
    
    # Initialize session state
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None
    
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    # Check if user is authenticated
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
        if 'code' in st.query_params:
            try:
                flow = create_flow()
                flow.fetch_token(code=st.query_params['code'])
                st.session_state.credentials = flow.credentials
                
                # Get user info
                user_info = get_user_info(flow.credentials)
                if user_info:
                    st.session_state.user_info = user_info
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error during authentication: {str(e)}")
    
    else:
        # Display user info
        if st.session_state.user_info:
            st.write(f"Welcome {st.session_state.user_info.get('name')}!")
            st.write(f"Email: {st.session_state.user_info.get('email')}")
            
            # Display profile picture
            if 'picture' in st.session_state.user_info:
                st.image(st.session_state.user_info['picture'], width=100)
            
            # Add logout button
            if st.button("Logout"):
                st.session_state.credentials = None
                st.session_state.user_info = None
                st.rerun()
            
            # Example of sending token to DRF backend
            if st.button("Send token to backend"):
                token_info = {
                    'token': st.session_state.credentials.token,
                    'refresh_token': st.session_state.credentials.refresh_token,
                    'token_uri': st.session_state.credentials.token_uri,
                    'client_id': st.session_state.credentials.client_id,
                    'client_secret': st.session_state.credentials.client_secret,
                    'scopes': st.session_state.credentials.scopes
                }
                st.write("Token info (to be sent to backend):")
                st.json(token_info)
                # TODO: Add your DRF API endpoint call here
                # response = requests.post('your-drf-api/auth/google/', json=token_info)

if __name__ == "__main__":
    main()