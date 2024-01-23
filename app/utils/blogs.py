import requests
import time
from datetime import datetime
import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_AVATAR = os.environ["DEFAULT_AVATAR"]

class Blog:

        # ----- Returning formatted date ----- #
    def format_date(date):
        date = datetime.strptime(date,
                                 "%Y-%m-%dT%H:%M:%S.%f")
        return date.strftime('%B %d, %Y %I:%M %p')

            # ----- Add a new blog post ----- #    
    def add_blog_post(headers, API_URL):
        
        with st.form("Blog Post Form", clear_on_submit=True):
            st.title("Post Something!")
            form_data = {"title": None, "content":None}
            form_data["title"] = st.text_input("Title:",
                                               placeholder="Title",
                                               label_visibility="collapsed")
            form_data["content"] = st.text_area("Write something:",
                                                placeholder="Write something...",
                                                label_visibility="collapsed")
            post = st.form_submit_button("Post", type="primary", use_container_width=True)
            if post:
                api_endpoint= f"{API_URL}/blogs/create"
                response = requests.post(api_endpoint, data=form_data, headers=headers)
                if response.status_code == 200:
                    data = response.json()["blog"]
                    with st.container(border=True):
                        with st.spinner("Loading.."):
                            time.sleep(1)
                            st.header(data["title"], divider=True)
                            st.write(Blog.format_date(data['date']))
                            st.write(f"@{data['author']}")
                            st.text(data["content"])
                elif response.status_code == 401:
                    st.error("Post failed")
                else:
                    st.error(f"Error: {response.status_code}")

            # ----- Show comments ----- #           
    def show_comments(API_URL, article_id):
            api_endpoint=f"{API_URL}/blogs/comments/read/article_id={article_id}"
            response = requests.get(api_endpoint)
            comments = response.json()
            for comment in comments:
                st.divider()
                st.write(f"""<span>
                            <img src='{DEFAULT_AVATAR}' width=20 height=20 style='vertical-align:middle'/> 
                            <b>{comment['owner']}</b>
                         </span>""",
                         unsafe_allow_html=True)
                st.write(Blog.format_date(comment['date']))
                st.write(comment["content"])
                st.divider()
                
            # ----- Show your own blogs in Profile ----- #
    def show_my_blogs(headers, API_URL):
        api_endpoint = f"{API_URL}/blogs/my_posts/all"
        response = requests.get(api_endpoint, headers=headers)
        try:
            if response.status_code == 200:
                posts = response.json()
                with st.container():
                    st.markdown("<h1 align='center'> My Posts 📑 </h1>", unsafe_allow_html=True)
                    for post in posts:
                        with st.container(border=True):
                            with st.spinner("Loading.."):
                                time.sleep(1)
                                st.header(post["title"], divider=True)
                                #date = datetime.strptime(post["date"], "%Y-%m-%dT%H:%M:%S.%f")
                                st.write(Blog.format_date(post['date']))
                                st.write(f"@{post['author']}")
                                st.text(post["content"])
                                with st.expander("Comments", expanded=False):
                                    Blog.show_comments(API_URL,article_id=post['_id'])
                                    
                        
            elif response.status_code == 404:
                st.error(response.json()["detail"])
            elif response.status_code == 401:
                st.error("Unauthorized. Please login")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Something went wrong with streamlit {e}")