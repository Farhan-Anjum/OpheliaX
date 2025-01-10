import streamlit as st
from google_auth_oauthlib.flow import Flow

def google_login():
    if 'google_auth' not in st.session_state:
        flow = Flow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['openid', 'email', 'profile']
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        st.markdown(f'[Login with Google]({authorization_url})')
    return st.session_state.get('google_auth', None)
