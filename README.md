Requirements
Make sure you have the following dependencies installed:

Scikit Learn
Pandas
Flask
You can install Flask version 2.2.2 using the following command:

bash
Copy code
pip install Flask==2.2.2
Running the Project
Navigate to the project home directory.

Run the Jupyter notebook "Movie Recommender.ipynb." This notebook will create a serialized version of the machine learning model.

After running the notebook, execute the following command in the terminal to start the Flask API:

bash
Copy code
python app.py
By default, Flask will run on port 5000.

Open your web browser and go to http://127.0.0.1:5000/ or http://localhost:5000.

You should now see the homepage of the Movie Recommender web application.

Enter the name of a movie in the text field and click "Submit."

If everything is set up correctly, you should receive a list of recommended movies on the HTML page.

Enjoy exploring movie recommendations with our Flask-based deployment!

Note
Ensure that you have a reliable internet connection and all dependencies are properly installed before running the project. If you encounter any issues, refer to the documentation of the respective libraries or Flask for assistance