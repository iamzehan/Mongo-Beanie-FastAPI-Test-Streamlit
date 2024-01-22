import requests
import time
from datetime import datetime
import streamlit as st

class Blog:
    
    def show_my_blogs(headers, API_URL):
        api_endpoint = f"{API_URL}/blogs/my_posts/all"
        response = requests.get(api_endpoint, headers=headers)
        try:
            if response.status_code == 200:
                posts = response.json()
                with st.container(border=True):
                    st.markdown("<h1 align='center'> Blogs </h1>", unsafe_allow_html=True)
                    
                    for post in posts:
                        with st.container(border=True):
                            with st.spinner("Loading.."):
                                time.sleep(1)
                                st.header(post["title"], divider=True)
                                date = datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S.%f")
                                st.write(date.strftime('%B %d, %Y %I:%M %p'))
                                st.write(f"@{post['author']}")
                                st.text(post["content"])
                        
            elif response.status_code == 404:
                st.error(response.json()["detail"])
            elif response.status_code == 401:
                st.error("Unauthorized. Please login")
            else:
                st.error(f"Error: {response.status_code}")
        except:
            st.error("Something went wrong with streamlit")