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