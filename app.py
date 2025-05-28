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

with open(output, 'rb') as f:
    similarity = pickle.load(f)

output2 = 'movies_dict.pkl'
file_id = st.secrets['movies_dict']
if not os.path.exists(output2):
    print("Downloading movies_dict.pkl from Google Drive...")
    gdown.download(id=file_id, output=output2, quiet=False)

with open(output2, 'rb') as f:
    movies = pd.DataFrame(pickle.load(f))


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://www.themoviedb.org/t/p/w500_and_h282_face/4j0PNHk9i6Y8v2w1n3f5a7c2z4h.jpg"


def recommend(movie, history=[]):
    if movie and movie not in history:
        history.append(movie)

    distances = np.zeros(len(similarity[0]))
    for m in history:
        idx = movies[movies['title'] == m].index[0]
        distances += similarity[idx]
    distances /= len(history)

    movie_index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    movies_list = [i for i in movies_list if i[0] != movie_index][:20]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')

if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

if 'history' not in st.session_state:
    st.session_state.history = []

# Selectbox with the currently selected movie as default
option = st.selectbox(
    "Search Similar Movies",
    movies['title'].values,
    index=movies[movies['title'] == st.session_state.selected_movie].index[0] if st.session_state.selected_movie else None,
    placeholder="Select a movie...",
)

if st.button("Recommend") or st.session_state.selected_movie:
    names, posters = recommend(option, st.session_state.history)
    num_movies = len(names)
    num_cols = 4
    rows = (num_movies + num_cols - 1) // num_cols

    # Inject CSS to hide all buttons and make them cover the card area
    st.markdown(
        """
        <style>
        /* Hide Streamlit buttons default style and stretch them */
        div.stButton > button {
            all: unset;
            width: 100%;
            height: 250px;
            cursor: pointer;
            display: block;
            position: relative;
            z-index: 2;
        }
        /* Make the card content unclickable, clicks go to the button */
        .movie-card {
            pointer-events: none;
            height: 250px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for row in range(rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            idx = row * num_cols + col_idx
            if idx < num_movies:
                with cols[col_idx]:
                    clicked = st.button("", key=f"movie_btn_{idx}", help="Click movie to select")

                    st.markdown(
                        f"""
                        <div class="movie-card">
                            <img src="{posters[idx]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;" />
                            <p style="
                                margin-top: 10px;
                                font-weight: bold;
                                overflow: hidden;
                                white-space: nowrap;
                                text-overflow: ellipsis;" title="{names[idx]}">
                                {names[idx]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if clicked:
                        st.session_state.selected_movie = names[idx]
                        st.experimental_rerun()
