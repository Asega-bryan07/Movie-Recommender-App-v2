# the dependencies to use 
import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours
from bs4 import BeautifulSoup
import requests, io
import PIL.Image
from urllib.request import urlopen
# import my_profile, about, mdbconnect # for sidebar



st.set_page_config(
    page_title="Movie Recommender App",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://wa.me/+254793681980',
        'Report a bug': "https://Asega-bryan07.git",
        'About': "This app is for the movie guys, Enjoy!"
    }

)

# Load profile images
profile_image = Image.open("profile/profile.jpg")
moviez = Image.open("profile/moviez.jpeg")
qrcode_img = Image.open("profile/qrcode.png")

# Sidebar options
sidebar_options = ["My Profile", "About the App"]

# Sidebar selection
selected_option = st.sidebar.selectbox("Developer", sidebar_options)

# Sidebar content
if selected_option == "My Profile":
    st.sidebar.image(qrcode_img, use_column_width=True)
    st.sidebar.markdown("ENG. BRYAN ASEGA")
    st.sidebar.markdown("Star and follow me on Github: https://github.com/Asega-bryan07")
    st.sidebar.markdown("View my LinkedIn: www.linkedin.com/in/asega-bryan-ba7781224")
    st.sidebar.markdown("Chat on Whatsapp: https://wa.me/+254793681980")
    st.sidebar.image(profile_image, use_column_width=True)
elif selected_option == "About the App":
    st.sidebar.image(moviez, use_column_width=True)
    st.sidebar.markdown("About")
    st.sidebar.markdown(
        "This app provides personalized movie recommendations based on your preferences."
    )
    st.sidebar.markdown('A user of the app has the ability to prompt for a movie of choice. This is an \
               upgrade from the previous version and therefore, Multiple genres and movies can be selected. \
               The app recommends movies based on the user\'s preferences and most importantly, it provides \
               a link to the movie\'s IMDB webpage for downloads and trailers. \
               Enjoy the app. Cheers! :)\n')
    st.sidebar.markdown('Created by: [ENG. ASEGA BRYAN](https://github.com/asega-bryan07/movie-recommender-app)')
    st.sidebar.markdown('Contact via email: [Almasibryan7@gmail.com]')
    st.sidebar.markdown("Copyright © 2024 AI+ | All rights reserved.")



with open('Data/movies.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open('Data/titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
header_ = {'User-Agent': 'Mozilla/5.0'}

def movie_poster_fetcher(imdb_link):
    ## Display Movie Poster
    url_data = requests.get(imdb_link, headers=header_).text
    s_data = BeautifulSoup(url_data, 'html.parser')
    
    # Find the IMDb link
    imdb_dp = s_data.find("meta", property="og:url")
    
    if imdb_dp is not None and 'content' in imdb_dp.attrs:
        imdb_link = imdb_dp.attrs['content']
        
        # Find the movie poster link
        movie_poster_dp = s_data.find("meta", property="og:image")
        
        if movie_poster_dp is not None and 'content' in movie_poster_dp.attrs:
            movie_poster_link = movie_poster_dp.attrs['content']
            
            u = urlopen(movie_poster_link)
            raw_data = u.read()
            image = PIL.Image.open(io.BytesIO(raw_data))
            image = image.resize((158, 301))
            st.image(image, use_column_width=False)
        else:
            st.warning("Movie poster link not found :(")
    else:
        st.warning("IMDb link not found :(")


def KNN_Movie_Recommender(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiating the KNN object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    model.fit() # run the model

    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
    print(table)
    return table




def run():
    img1 = Image.open('profile/movies.jpeg')
    img1 = img1.resize((250, 250), )
    st.image(img1, use_column_width=False)
    st.title("Movie Recommender App")
    st.markdown('''<h4 style='text-align: left; color: #90EE90;'>Your #1 Movie Recommender App 👌</h4>''',
                unsafe_allow_html=True)
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['Your Selection >>', 'Movie based', 'Genre based']
    cat_op = st.selectbox('Select Type for Recommendation', category)
    if cat_op == category[0]:
        st.warning("You have't selected any type...")
    elif cat_op == category[1]:
        select_movie = st.selectbox('Select movie: (Type for Recommendation)',
                                    ['--Select--'] + movies)
        dec = st.radio("Include Movie Posters?", ('Yes', 'No'))
        st.markdown(
            '''<h4 style='text-align: left; color: #3498db;'> Just a moment...</h4>''',
            unsafe_allow_html=True)
        if dec == 'No':
            if select_movie == '--Select--':
                st.warning('Please Select a Movie!!')
            else:
                no_of_reco = st.slider('Number of movies to Recommended:', min_value=4, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
                table.pop(0)
                c = 0
                st.success('Your Choices from our Recommendation')
                cols = st.columns(4)
                for movie, link, ratings in table:
                    with cols[c % 4]:
                        st.markdown(f"[ {movie}]({link})")
                        st.markdown('Movie Rating: ' + str(ratings) + '\u2B50')
                    c += 1
        else:
            if select_movie == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.slider('Number of movies Recommended:', min_value=4, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
                table.pop(0)
                c = 0
                st.success('Your Choices from our Recommendation')
                cols = st.columns(4)
                for movie, link, ratings in table:
                    with cols[c % 4]:
                        st.markdown(f"[ {movie}]({link})")
                        movie_poster_fetcher(link)
                        st.markdown('Movie Rating: ' + str(ratings) + '\u2B50')
                    c += 1
    elif cat_op == category[2]:
        sel_gen = st.multiselect('Select Genre(s):', genres)
        dec = st.radio("Include Movie Posters?", ('Yes', 'No'))
        st.markdown(
            '''<h4 style='text-align: left; color: #3498db;'>Just a moment...</h4>''',
            unsafe_allow_html=True)
        if dec == 'No':
            if sel_gen:
                imdb_score = st.slider('Choose by Rating LEvel', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies:', min_value=4, max_value=20, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Your Choices from our Recommendation')
                cols = st.columns(4)
                for movie, link, ratings in table:
                    with cols[c % 4]:
                        st.markdown(f"[ {movie}]({link})")
                        st.markdown('Movie Rating: ' + str(ratings) + '\u2B50')
                    c += 1
        else:
            if sel_gen:
                imdb_score = st.slider('Choose by Rating LEvel', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies:', min_value=4, max_value=20, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Your Choices from our Recommendation')
                cols = st.columns(4)
                for movie, link, ratings in table:
                    with cols[c % 4]:
                        st.markdown(f"[ {movie}]({link})")
                        movie_poster_fetcher(link)
                        st.markdown('Movie Rating: ' + str(ratings) + '\u2B50')
                    c += 1
                '''Release Version 2.0.1'''

run()

