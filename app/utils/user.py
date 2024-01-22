import requests
import streamlit as st
from utils.blogs import Blog
from email_validator import validate_email

class User:
    def login(API_URL):
        with st.form("Login form",clear_on_submit=False):
            st.header("Login")
            form_data = {"username":None, 
                "password": None}
            form_data["username"]=st.text_input("username")
            form_data["password"]=st.text_input("password", type="password")
            submit = st.form_submit_button("Login",use_container_width=True)
            
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

        # API endpoint
        api_endpoint = f"{API_URL}/user/me"  # replace with your actual API endpoint

        # Headers with the access token
        headers = {"Authorization": f"Bearer {access_token}"}

        # Make GET request to the API endpoint
        response = requests.get(api_endpoint, headers=headers)
        user_info = response.json()
        # Check if the request was successful
        if response.status_code == 200:
            
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.image("https://cdn-icons-png.flaticon.com/512/1053/1053244.png", width=200)
                with col2:
                    edit = st.button("✏️ Edit Profile", type="primary", use_container_width=True)
                    if edit:
                        with st.form("Profile Edit Form", clear_on_submit=False):
                            username = st.text_input(label="Username: ", value=user_info["username"])
                            name = st.text_input(label="Name: ", value=user_info["full_name"])
                            email = st.text_input(label="Email: ", value=user_info["email"])
                            update = st.form_submit_button(label="💾 Update Profile", use_container_width=True, type="primary")
                        cancel=st.button("Cancel", use_container_width=True)
                    else:
                        st.write("<b>Username:</b>", user_info["username"], unsafe_allow_html=True)
                        st.write("<b>Name:</b>", user_info["full_name"], unsafe_allow_html=True)
                        st.write("<b>Email:</b>", user_info["email"], unsafe_allow_html=True)
                    
        
        elif response.status_code == 401:
            st.error("Unauthorized. Please login")
        else:
            st.error(f"Error: {response.status_code}")
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                my_posts = st.button(":red[My Posts 📑]",use_container_width=True)
            with col2:
                pictures = st.button("Pictures 🖼️", use_container_width=True)
            with col3:
                update_profile=st.button("Edit Profile ✏️",type="primary", use_container_width=True)
            
        if my_posts:            
            Blog.show_my_blogs(headers, API_URL)
        if pictures:
            st.error("No pictures yet")
        if update_profile:
            with st.form("Profile Edit Form", clear_on_submit=False):
                username = st.text_input(label="Username: ", value=user_info["username"])
                name = st.text_input(label="Name: ", value=user_info["full_name"])
                email = st.text_input(label="Email: ", value=user_info["email"])
                update = st.form_submit_button(label="Update Profile", use_container_width=True, type="primary")
        else:
            Blog.show_my_blogs(headers,API_URL)
        
