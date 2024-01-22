import os
from utils.profile import User

from dotenv import load_dotenv
import requests
import streamlit as st


load_dotenv()
API_URL = os.environ['API_URL']


with st.sidebar:
    pages = st.selectbox(label="Pages", options=["Login", "Profile", "Sign up"])
    if pages== "Login":
        User.login(API_URL)
if pages == "Sign up":
        User.signup(API_URL)
if pages == "Profile":
    try:
        access_token=st.session_state.access_token
        
    except:
        access_token=None
        User.show_profile(access_token, API_URL)

    

        
        
    


    
        