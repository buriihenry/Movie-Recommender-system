## Deploying our Model using Flask
In this project I will show you how to deploy ML model using Flask 

### Requirements
You must have Scikit Learn, Pandas and Flask installed.

Flask version: 2.2.2
pip install Flask==2.2.2

### Running the project
1. Ensure that you are in the project home directory. Run the notebook "Movie Recommender.ipynb" first

This would create a serialized version of our model

2. Run app.py using below command to start Flask API
```
python app.py
```
By default, flask will run on port 5000.

3. Navigate to URL http://127.0.0.1:5000/ (or) http://localhost:5000

You should be able to view the homepage.

Enter the movie name in the text field and hit Submit.

If everything goes well, you should  be able to see recommended movies on the HTML page!

Hit Star if you like this project:

