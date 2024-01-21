import os
from email_validator import validate_email
from dotenv import load_dotenv
import requests
import streamlit as st


load_dotenv()
API_URL = os.environ['API_URL']


with st.sidebar:
    pages = st.selectbox(label="Pages", options=["Login", "Profile", "Sign up"])

if pages=="Login":
    with st.form("Login form"):
        st.header("Login")
        form_data = {"username":None, 
            "password": None}
        form_data["username"]=st.text_input("username")
        form_data["password"]=st.text_input("password", type="password")
        submit = st.form_submit_button("Login")
        
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
                
            elif response.status_code == 401:
                st.error("Incorrect username or password. Please try again.")
            else:
                st.error(f"Error: {response.status_code}")
        
if pages == "Profile":
    @st.cache_data
    def show_blogs(headers):
        api_endpoint = f"{API_URL}/blogs/my_posts/all"
        response = requests.get(api_endpoint, headers=headers)
        try:
            if response.status_code == 200:
                posts = response.json()
                st.markdown("<h1 align='center'> Blogs </h1>", unsafe_allow_html=True)
                for post in posts:
                    st.header(post["title"])
                    st.write(post["date"])
                    st.divider()
                    st.subheader(f"@{post['author']}")
                    st.text(post["content"])
            elif response.status_code == 404:
                st.error(response.json()["detail"])
            elif response.status_code == 401:
                st.error("Unauthorized. Please provide a valid access token.")
            else:
                st.error(f"Error: {response.status_code}")
        except:
            st.error("Something went wrong with streamlit")
        
    def show_profile(access_token):
        # API endpoint
        api_endpoint = f"{API_URL}/user/me"  # replace with your actual API endpoint

        # Headers with the access token
        headers = {"Authorization": f"Bearer {access_token}"}

        # Make GET request to the API endpoint
        response = requests.get(api_endpoint, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            user_info = response.json()
            
            st.write("Username:", user_info["username"])
            st.write("Full name:", user_info["full_name"])
            st.write("Email:", user_info["email"])
            # Add more user information fields as needed
        elif response.status_code == 401:
            st.error("Unauthorized. Please provide a valid access token.")
        else:
            st.error(f"Error: {response.status_code}")
        
        profile_details = st.radio("",["My Posts", "Pictures"])
        
        if profile_details=="My Posts":
            show_blogs(headers)
        else:
            st.error("No pictures yet")
        
  
    try:
        access_token=st.session_state.access_token
        show_profile(access_token)
    except:
        st.error("Please login")

if pages == "Sign up":
    with st.form("Sign up form"):
        st.header("Create an account!")
        username = st.text_input("Username:", placeholder="johndoe123")
        full_name = st.text_input("Full name:", placeholder="John Doe")
        try:
            email = st.text_input(label="Email:", placeholder="johndoe@example.com")
            if email:
                validate_email(email, check_deliverability=False)
                st.success("Email is valid")
        except:
            st.error("Email not valid")
            
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if password == confirm_password:
            st.success("Passwords match")
        else:
            raise st.error("Passwords don't match")
        
        signup = st.form_submit_button("Sign up")

        
        
    


    
        