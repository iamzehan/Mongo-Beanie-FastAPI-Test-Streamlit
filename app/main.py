import os
import requests
import streamlit as st
from utils.user import User
from dotenv import load_dotenv

def main(API_URL):
    with st.sidebar:
        pages = st.selectbox(label="Pages", options=["Login", "Profile", "Sign up"])
        if pages== "Login":
            User.login(API_URL)
    if pages == "Sign up":
            User.signup(API_URL)
    if pages == "Profile":
        try:
            access_token=st.session_state.access_token
            User.show_profile(access_token, API_URL)
            
        except:
            access_token=None
            User.show_profile(access_token, API_URL)

if __name__ == "__main__":
    load_dotenv()
    API_URL = os.environ['API_URL']
    main(API_URL)
    

        
        
    


    
        