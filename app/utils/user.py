import requests
import streamlit as st
from utils.blogs import Blog
from email_validator import validate_email
import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_AVATAR = os.environ["DEFAULT_AVATAR"]

class User:
    def get_headers(access_token):
        return {"Authorization": f"Bearer {access_token}"}
    
    def login(API_URL):
        with st.form("Login form",clear_on_submit=False):
            st.header("Login")
            form_data = {"username":None, 
                "password": None}
            form_data["username"]=st.text_input("username")
            form_data["password"]=st.text_input("password",
                                                type="password")
            submit = st.form_submit_button("Login",
                                           use_container_width=True)
            
            # Login button
            if submit:
                # API endpoint
                api_endpoint = f"{API_URL}/user/login"  # replace with your actual API endpoint
                # Make POST request to the API endpoint
                response = requests.post(api_endpoint, data=form_data)
                data = response.json()

                # Check if the request was successful
                if response.status_code == 200:
                    st.success("Login successful!")
                    st.session_state.access_token = data["access_token"]
                    st.session_state.refresh_token = data["refresh_token"]
                    st.session_state.logged_in = True
                    
                elif response.status_code == 401:
                    st.error("Incorrect username or password. Please try again.")
                else:
                    st.error(f"Error: {response.status_code}")
    
    def signup(API_URL):
        with st.form("Sign up form", clear_on_submit=False):
            st.header("Create an account!")
            username = st.text_input("Username:", placeholder="johndoe123")
            full_name = st.text_input("Full name:", placeholder="John Doe")
            email = st.text_input(label="Email:", placeholder="johndoe@example.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup = st.form_submit_button("Sign up",use_container_width=True)
            # we have to create a function that does some checking of the form let's name it check_form()
            if (password and confirm_password) and (password == confirm_password):
                    st.success("Passwords match")
            else:
                st.error("Please enter valid password")
                  
    def show_profile(access_token, API_URL):
        
        def show_user_info(user_info):
            
            st.header("User Info")
            st.divider()
            
            st.write(f"<b>Username:</b>",
                     user_info["username"],
                     unsafe_allow_html=True)
            
            st.write("<b>Name:</b>",
                     user_info["full_name"],
                     unsafe_allow_html=True)
            
            st.write("<b>Email:</b>",
                     user_info["email"],
                     unsafe_allow_html=True)

        api_endpoint = f"{API_URL}/user/me"

        # Getting the headers "Bearer <Token>"
        headers = User.get_headers(access_token)

        # Make GET request to the API endpoint for Profile
        response = requests.get(api_endpoint, headers=headers)
        user_info = response.json()
        
        # Check if the request was successful
        if response.status_code == 200:
            
            with st.container(border=True):
                col1, _, col3 = st.columns([3, 3, 4])
                with col1:
                    st.image(F"{DEFAULT_AVATAR}", use_column_width=True)
                    st.divider()
                    edit = st.button("✏️ Edit Profile", type="primary", use_container_width=True)
                with col3:
                    if edit:
                        with st.form("Profile Edit Form", clear_on_submit=False):
                            username = st.text_input(label="Username: ", value=user_info["username"])
                            name = st.text_input(label="Name: ", value=user_info["full_name"])
                            email = st.text_input(label="Email: ", value=user_info["email"])
                            update = st.form_submit_button(label="💾 Update Profile", use_container_width=True, type="primary")
                            if update:
                                show_user_info(user_info)
                                
                        cancel=st.button("Cancel", use_container_width=True)
                        
                        if cancel:
                            show_user_info(user_info)
                    
                    else:
                        show_user_info(user_info)
                        
            # --- Adding Blog Post from Profile Page --- #
            posted = Blog.add_blog_post(headers=headers, API_URL=API_URL)
            
            # --- Navigating through different options in profile page --- #
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)
                with col2:
                    my_posts = st.button(":red[My Posts 📑]",use_container_width=True)
                with col3:
                    pictures = st.button("Pictures 🖼️", use_container_width=True)
            
            if my_posts or posted:            
                Blog.show_my_blogs(headers, API_URL)
            if pictures:
                st.error("No pictures yet")
            
        elif response.status_code == 401:
            st.error("Unauthorized. Please login")
        else:
            st.error(f"Error: {response.status_code}")