## Intro
With the rise of digital entertainment, movies have become a popular form of entertainment, with an endless variety of genres and styles. However, with so many options available, finding the perfect movie can be overwhelming. To solve this problem, a movie recommender system can be used to help people find the perfect movie for their preferences. This article explores the creation of a movie recommender system using the Flask framework and the code is available on Github.

## The Problem:

There are a lot of movies available for people to watch, and the number is only increasing every day. With so many options, it can be difficult for users to find movies that they will enjoy. The problem is even more pronounced when you consider that people have different preferences and tastes.

## The Solution:

A movie recommender system is a solution to this problem. It provides users with recommendations based on their preferences and past behavior. By analyzing data such as the movies people have watched in the past, the movie recommender system can make recommendations that are tailored to the user’s interests.


## Deploying our Model using Flask
In this project I will show you how to deploy ML model using Flask 

### Requirements
1. Python 3.10
2. Scikit Learn 
3. Pandas and 
4. Flask

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