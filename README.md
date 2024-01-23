# Testing a FastAPI+MongoDB based API with Streamlit frontend

Previously, we have implemented an [API](https://github.com/iamzehan/FastAPI-Beanie-MongoDB) combining the power of FastAPI, BeanieODM & MongoDB. We learned how to perform Create, Read, Update, Delete operations along with JWT & Oauth2 authorization enabled features. Finally, we dockerized the whole project and published it in our local docker engine container.

### What do we do in this project?
___
Since, we have learned how to create an API, it is necessary to test the endpoints with requests sent from the frontend. We are using [Streamlit](https://streamlit.io/) which is a Python based framework; it that allows us to build data apps fast. We only want to perform requests on our API Endpoints, so we are not using any complicated frontend frameworks. 
```
📁 app
|   |___ 📁 utils
|   |       |___ __init__.py
|   |       |___ blogs.py
|   |       |___ user.py
|   |___ ⚙️ .env
|   |___ main.py
🗒️requirements.txt


```

### [`📁 app`](https://github.com/iamzehan/Mongo-Beanie-FastAPI-Test-Streamlit/tree/main/app)
Contains the entirety of the app.

* ### [`📁 utils`](https://github.com/iamzehan/Mongo-Beanie-FastAPI-Test-Streamlit/tree/main/app/utils)

Contains different features and performs requests in different routes. Requests made in similar routes are clustered together in one file.

* #### <img src="https://upload.wikimedia.org/wikipedia/commons/0/0a/Python.svg" alt="html5" width="20" height="20" style="vertical-align: middle"/> [`blogs.py`](https://github.com/iamzehan/Mongo-Beanie-FastAPI-Test-Streamlit/blob/main/app/utils/blogs.py)
    * Formats date - `fromat_date()`
    * `GET` User's own blog list request. - `show_my_blogs()`
    * `GET` Blog specific omments section request - `show_comments()`.
    * `POST` Blog Post request. - `add_blog_post()`

* #### <img src="https://upload.wikimedia.org/wikipedia/commons/0/0a/Python.svg" alt="html5" width="20" height="20" style="vertical-align: middle"/> [`user.py`](https://github.com/iamzehan/Mongo-Beanie-FastAPI-Test-Streamlit/blob/main/app/utils/user.py)

    * JWT Authorization header - `get_headers()`
    * `POST` User Login - `login()`
    * `POST` User Signup - `signup()`
    * `GET` User Profile - `show_profile()`

* ### <img src="https://upload.wikimedia.org/wikipedia/commons/0/0a/Python.svg" alt="html5" width="20" height="20" style="vertical-align: middle"/> [`main.py`](https://github.com/iamzehan/Mongo-Beanie-FastAPI-Test-Streamlit/blob/main/app/main.py)

    * Runs the app with `streamlit run main.py` command
    * Makes other pages available with side bar selectbox.

### 🗒️requirements.txt
Contains the dependencies.

<h3 align="center"> Technologies & Links </h3>

___

<p align="center"> 
<a href="https://streamlit.io/" title="FastAPI" target="_blank"><img src="https://styles.redditmedia.com/t5_7ispo3/styles/communityIcon_kxy2jy8mz8aa1.png" alt="html5" width="40" height="40"/></a> 
<img src="https://upload.wikimedia.org/wikipedia/commons/0/0a/Python.svg" alt="html5" width="40" height="40"/>
</p>
