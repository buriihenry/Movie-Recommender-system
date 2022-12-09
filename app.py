# Importing the necessary libraries
from flask import Flask, request, render_template
from flask_cors import cross_origin
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
from tmdbv3api import TMDb, Movie
import requests

# Initialising flask app
app = Flask(__name__)

# load the data
df = pd.read_csv('Data/preprocessed_data.csv')
# load cache data
df_cache = pd.read_csv('Data/cache_data.csv')
# storing movie title into list
movie_list = list(df['movie_title'])

# creating TMDB Api Object
tmdb = TMDb()
tmdb.api_key = 'e955d66146c91573e52a09a5566459d4'

# This Function take movie name list and return their Poster link, Tag Line and Title into dictionary
def get_poster_link(title_list):
    """
    This Function take movie name list and return their Poster link, Tag line and Title into dictionary.
    """
    # TMDB Movie Api Object
    tmdb_movie = Movie()

    # Storing data in to dictionary
    dic_data = {"Movie_Title": [], "Poster_Links": [], "Tag_line": []}

    for title in title_list:
        # checking given movie is present in our cache database or not.
        r_df = df_cache[df_cache['Title'] == title]
        try:
            # if given movie is found in our cache database then run this part
            if len(r_df) >= 1:
                dic_data["Movie_Title"].append(r_df['Movie_Title'].values[0])
                dic_data["Poster_Links"].append(r_df['Poster_Links'].values[0])
                dic_data["Tag_Line"].append(r_df['Tag_Line'].values[0])

            # otherwise retrieve the data from tmdbi api
            else:
                result = tmdb_movie.search(title)
                movie_id = result[0].id
                response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
                data_json = response.json()

                # Fetching movie title and poster link
                movie_title = data_json['title']
                movie_poster_link = "https://image.tmdb.org/t/p/original" + data_json['poster_path']
                movie_tag_line = data_json['tagline']

                # Appending movie title and poster link into dictionary
                dic_data['Movie_Title'].append(movie_title)
                dic_data['Poster_Links'].append(movie_poster_link)
                dic_data['Tag_Line'].append(movie_tag_line)
        except:
            pass        
    return dic_data
@app.route('/', methods=['GET']) #route to display homepage
@cross_origin()
def home():
    return render_template('index.html')
     