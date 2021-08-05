from flask import Flask
from dotenv import load_dotenv # loads variables from .env
from flask_cors import CORS # Cross origin resource sharing - allows request from same computer?
import os # module provides functions for interating with the operatin system  (command line stuff) 

#from flask_sqlalchemy import SQLAlchemy  - don't have a db - don't need now
# from flask_migrate import Migrate  # if no models, prob don't need this either

# UPLOAD_FOLDER = '/Users/ada/Developer/projects/capstone/BirdNET/example'  # moved to .venv

# db = SQLAlchemy()  # - don't need this
# migrate = Migrate() # nope?

load_dotenv()  # calls variables (that are text) from .env and converts
                # them into real variables so git doesn't track them? like an API key

def create_app(test_config=None):
    app = Flask(__name__)
    # to keep order of sorted dictionary passed to jsonify() function
    app.config['JSON_SORT_KEYS'] = False 
   
    app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")

    # track modifications for database tables?
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # if test_config is None: 
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_DATABASE_URI")
    # else:
    #     app.config["TESTING"] = True
    #     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    #         "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.example_model import ExampleModel  ## example_model is a file
    ## this grabs my models, where my routes are and my blueprints   
    ## (grabbing it all from everywhere) to be able to run my app

    # PROB DON'T NEED THIS IF NO MODELS
    # from app.models.file import File
    # from app.models.file_collection import FileCollection

    # INITIALIZES DATABASE
    # db.init_app(app)
    # i think this updates the models everytime I run flask run
    # migrate.init_app(app, db)


    # Importing all routes from each model
    from .routes import bird_bp
    # from .routes import card_bp    
    
    # Register Blueprints for each route
    app.register_blueprint(bird_bp)

    CORS(app) # WHAT DOES THIS DO?

    # IF ALL GOES WELL, HERE YOU APP IS READY TO work and do posts! 
    # gets, deletes, or whatever your API does!
    return app