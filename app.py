# Importing modules
from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
from tmdbv3api import TMDb, Movie
import requests
import logging
import os
from functools import lru_cache
from typing import Dict, List, Optional
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    TMDB_API_KEY = 'e955d66146c91573e52a09a5566459d4'
    CACHE_SIZE = 128
    SIMILARITY_CACHE_FILE = 'Data/similarity_matrix.npy'
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

# Initialising flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize TMDB API
tmdb = TMDb()
tmdb.api_key = Config.TMDB_API_KEY

def load_data() -> tuple:
    """Load and prepare the movie data."""
    try:
        df = pd.read_csv('Data/preprocessed_data.csv')
        df_cache = pd.read_csv('Data/cache_data.csv')
        movie_list = list(df['movie_title'])
        return df, df_cache, movie_list
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

# Load data
try:
    df, df_cache, movie_list = load_data()
except Exception as e:
    logger.error(f"Failed to load data: {str(e)}")
    raise

@lru_cache(maxsize=Config.CACHE_SIZE)
def compute_similarity_matrix() -> tuple:
    """Compute and cache the similarity matrix."""
    try:
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df['comb'])
        cosine_sim = cosine_similarity(count_matrix)
        return cosine_sim, cv
    except Exception as e:
        logger.error(f"Error computing similarity matrix: {str(e)}")
        raise

def validate_movie_title(title: str) -> Optional[str]:
    """Validate and correct movie title."""
    if not title or not isinstance(title, str):
        return None
    
    title = title.lower().strip()
    matches = get_close_matches(title, movie_list, n=3, cutoff=0.6)
    return matches[0] if matches else None

def get_poster_link(title_list: List[str]) -> Dict[str, List[str]]:
    """
    Fetch movie metadata from TMDB API with caching and error handling.
    
    Args:
        title_list: List of movie titles to fetch metadata for
        
    Returns:
        Dictionary containing movie titles, poster links, and taglines
    """
    tmdb_movie = Movie()
    dic_data = {"Movie_Title": [], "Poster_Links": [], "Tag_Line": []}
    
    for title in title_list:
        try:
            # Check cache first
            r_df = df_cache[df_cache['Title'] == title]
            if len(r_df) >= 1:
                dic_data["Movie_Title"].append(r_df['Movie_Title'].values[0])
                dic_data["Poster_Links"].append(r_df['Poster_Links'].values[0])
                dic_data["Tag_Line"].append(r_df['Tag_Line'].values[0])
                continue

            # Fetch from TMDB API with retries
            for attempt in range(Config.MAX_RETRIES):
                try:
                    result = tmdb_movie.search(title)
                    if not result:
                        logger.warning(f"No results found for movie: {title}")
                        break
                        
                    movie_id = result[0].id
                    response = requests.get(
                        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}',
                        timeout=5
                    )
                    response.raise_for_status()
                    data_json = response.json()

                    dic_data['Movie_Title'].append(data_json['title'])
                    dic_data['Poster_Links'].append(
                        f"https://image.tmdb.org/t/p/original{data_json['poster_path']}"
                    )
                    dic_data['Tag_Line'].append(data_json.get('tagline', ''))
                    break
                except requests.exceptions.RequestException as e:
                    if attempt == Config.MAX_RETRIES - 1:
                        logger.error(f"Failed to fetch data for {title}: {str(e)}")
                    time.sleep(Config.RETRY_DELAY)
                    
        except Exception as e:
            logger.error(f"Error processing movie {title}: {str(e)}")
            continue

    return dic_data

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
@cross_origin()
def recommendation():
    """Handle movie recommendations."""
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    try:
        # Get and validate input
        title = request.form.get('search', '').strip()
        if not title:
            return render_template('error.html', error="Please enter a movie title")

        # Validate and correct movie title
        correct_title = validate_movie_title(title)
        if not correct_title:
            return render_template('error.html', error="Movie not found")

        # Get similarity matrix
        cosine_sim, _ = compute_similarity_matrix()

        # Get movie index and similarity scores
        idx = df['movie_title'][df['movie_title'] == correct_title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort and get top 15 similar movies
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[0:15]
        suggested_movies = [df['movie_title'][i[0]] for i in sim_scores]

        # Get movie metadata
        poster_data = get_poster_link(suggested_movies)
        return render_template('recommended.html', output=poster_data)

    except Exception as e:
        logger.error(f"Error in recommendation: {str(e)}")
        return render_template('error.html', error="An error occurred while processing your request")

if __name__ == '__main__':
    logger.info("Starting Movie Recommendation App")
    app.run(debug=True)