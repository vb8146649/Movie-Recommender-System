import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
import gdown
import os

api_key = st.secrets['api_key']

output = 'similarity.pkl'
file_id = st.secrets['similarity']
if not os.path.exists(output):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(id=file_id, output=output, quiet=False)

# Now load the file
with open(output, 'rb') as f:
    similarity = pickle.load(f)

output2 = 'movies_dict.pkl'
file_id = st.secrets['movies_dict']
if not os.path.exists(output2):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(id=file_id, output=output2, quiet=False)

# Now load the file
with open(output2, 'rb') as f:
    movies = pd.DataFrame(pickle.load(f))

# movies= pd.DataFrame(pickle.load(open('movies_dict.pkl', 'rb')))
# similarity = pickle.load(open('similarity.pkl', 'rb'))
import requests
import streamlit as st

def fetch_poster(movie_id):
    api_key = st.secrets['api_key'] # Replace with your actual API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    # st.text(data)  # Optional debug print
    if 'poster_path' in data and data['poster_path']:
        poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        # st.text(poster_url)  # Optional debug print
        return poster_url
    else:
        # Fallback poster image
        return "https://www.themoviedb.org/t/p/w500_and_h282_face/4j0PNHk9i6Y8v2w1n3f5a7c2z4h.jpg"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:20]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.title('Movie Recommender System')


option = st.selectbox(
    "Search Similar Movies",
    movies['title'].values,
    index=None,
    placeholder="Select contact method...",
)

if st.button("Recommend"):
    names, posters = recommend(option)
    
    num_movies = len(names)
    num_cols = 4
    rows = (num_movies + num_cols - 1) // num_cols

    for row in range(rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            idx = row * num_cols + col_idx
            if idx < num_movies:
                with cols[col_idx]:
                    st.markdown(
                        f"""
                        <div style="height: 250px; text-align: center;">
                            <img src="{posters[idx]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;" />
                            <p style="
                                margin-top: 10px;
                                font-weight: bold;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;
                            " title="{names[idx]}">
                                {names[idx]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
