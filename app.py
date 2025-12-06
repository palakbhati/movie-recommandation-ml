import streamlit as st
import pandas as pd
import requests
import pickle
import joblib
import os

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None  # In case poster is missing

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Load movies
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Load similarity matrix (compressed with joblib)
if not os.path.exists("similarity.pkl"):
    st.error("Error: similarity.pkl not found. Please make sure the file is in the project folder.")
else:
    similarity = joblib.load("similarity.pkl")

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)

        columns = [col1, col2, col3, col4, col5]
        for idx, col in enumerate(columns):
            col.text(recommended_movie_names[idx])
            if recommended_movie_posters[idx]:
                col.image(recommended_movie_posters[idx])
            else:
                col.text("Poster not available")
 