# 🎬 Movie Recommender System

This is a **Movie Recommender System** built with [Streamlit](https://streamlit.io/). The app suggests similar movies based on your selected favorite using a precomputed similarity matrix and movie metadata. Posters are fetched using The Movie Database (TMDB) API.

👉 **[Click here to use the app](https://vb8146649-movie-recommender-system-app-fbmttm.streamlit.app/)**  

---
## 📸 Screenshots

### 🔍 Movie Search 
<img src="https://github.com/vb8146649/Movie-Recommender-System/blob/main/demo.gif" alt="movie-recommender-demo" width=600 height=600>

---

## 🔗 Links

- 📓 **Google Colab Notebook (Model Training)**: 
    - [Open in Colab](https://colab.research.google.com/drive/1msvrnYLSlZMDFCZj01TSjpkNtMVtttXx?usp=sharing)
- 🏷️ **Model Files on Kaggle**: 
    - [Movies Dataset](https://www.kaggle.com/datasets/makray/tmdb-5000-movies)
    - [Credits Dataset](https://www.kaggle.com/datasets/kryusufkaya/tmdb-5000-credits) 

---

## 🚀 Features

- Search and select a movie title
- Get up to 20 similar movie recommendations
- View posters fetched dynamically using TMDB API
- Fast loading through optimized `.pkl` model files hosted on Google Drive

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Requests](https://docs.python-requests.org/)
- [gdown](https://pypi.org/project/gdown/)
- Google Drive for model file storage
- TMDB API for movie poster retrieval

---

## 🔐 Secrets Configuration

Create a `.streamlit/secrets.toml` file for sensitive keys:

```toml
api_key = "your_tmdb_api_key"
similarity = "your_google_drive_file_id_for_similarity.pkl"
movies_dict = "your_google_drive_file_id_for_movies_dict.pkl"
