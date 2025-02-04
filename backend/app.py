from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.user import User
from models.video_game import VideoGame
from models.loans import Loan

app = Flask(__name__)  # - create a flask instance
# - enable all routes, allow requests from anywhere (optional - not recommended for security)
CORS(app, resources={r"/*": {"origins": "*"}})

# Specifies the database connection URL. In this case, it's creating a SQLite database
# named 'library.db' in your project directory. The three slashes '///' indicate a
# relative path from the current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)  # initializes the databsewith the flask application


# this is a decorator from the flask module to define a route for adding a book, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/video_games', methods=['POST'])
def add_video_game():
    data = request.json  # this is parsing the JSON data from the request body
    new_video_game = VideoGame(
        name=data['name'],  # Set the title of the new book.
        creator=data['creator'],  # Set the author of the new book.
        year_published=data['year_published'],
        # Set the types(fantasy, thriller, etc...) of the new book.
        type=data['type']
        # add other if needed...
    )
    db.session.add(new_video_game)  # add the bew book to the database session
    db.session.commit()  # commit the session to save in the database
    return jsonify({'message': 'Video game added to database.'}), 201


# a decorator to Define a new route that handles GET requests
@app.route('/video_games', methods=['GET'])
def get_video_games():
    try:
        video_games = VideoGame.query.all()  # Get all the books from the database

        # Create empty list to store formatted book data we get from the database
        video_games_list = []

        for video_game in video_games:  # Loop through each book from database
            video_game_data = {  # Create a dictionary for each book
                'id': video_game.id,
                'name': video_game.name,
                'creator': video_game.creator,
                'year_published': video_game.year_published,
                'type': video_game.type
            }
            # Add the iterated book dictionary to our list
            video_games_list.append(video_game_data)

        return jsonify({  # Return JSON response
            'message': 'Video games retrieved successfully',
            'video games': video_games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve video games',
            'message': str(e)
        }), 500  #


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your  models(check the models folder)

    with app.test_client() as test:
        response = test.post('/video_games', json={  # Make a POST request to /books endpoint with book  data
            'name': 'Fortnite',
            'creator': 'my dad',
            'year_published': 1997,
            'type': 'Horror'  # let's say 1 is fantasy
        })
        print("Testing /video_games endpoint:")
        # print the response from the server
        print(f"Response: {response.data}")

        #  GET test here
        get_response = test.get('/video_games')
        print("\nTesting GET /video_games endpoint:")
        print(f"Response: {get_response.data}")

    app.run(debug=True)  # start the flask application in debug mode

    # DON'T FORGET TO ACTIVATE THE ENV FIRST:
    # /env/Scripts/activate - for windows
    # source ./env/bin/activate - - mac
