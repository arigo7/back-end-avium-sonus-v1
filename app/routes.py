from flask import Blueprint, request, jsonify, make_response, flash, \
    request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app.parse_txt_file_json import get_file_name, parse_output_file
# from app import db
# from app.models.file import File 
# from app.models.file_collection import Collection
# from sqlalchemy import asc, desc # to add feature to sort - PROB WON'T USE
import json
import time

# Allowed extensions that BirdNET can handle
ALLOWED_EXTENSIONS = {'wav', 'm4a'}
def allowed_file(filename):
    '''
    input: file with extension .wav or .m4a
    output: returns true or false if file extension is allowed
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS

bird_bp = Blueprint("bird", __name__, url_prefix="/")

# JSON FILE - ROUTE - route function sends successful connection response
#####################################################################
@bird_bp.route("/jsonfile", methods=['GET'], strict_slashes=False)
def display_json():
    
    path = f"/Users/ada/Developer/projects/capstone/back-end-avium-sonus-v1/test2.json"
    with open (path) as json_file:
        data = json.load(json_file)
    return jsonify(data), 200

# HOME - ROUTE - route lets you into the gates of Avium Sonus
#####################################################################
@bird_bp.route("", methods=['GET'], strict_slashes=False)
def welcome_message():
    welcome_message = 'Welcome to Avium Sonus'
    return make_response(welcome_message, 200)


@bird_bp.route("/bird_stream", methods=['GET', 'POST'], strict_slashes=False)
def upload_audio():
    if request.method == 'POST':
        # check if the post request has the file part
        if not request.stream:
            flash('No stream part')
            return redirect(request.url) # redirect to where request was sent from

        # here add latitude and longitude upload
        lat, lon = 47.34, -122.890
        

        # secure_filename returns a secure version of it, then the 
        # file(now 'filename') can safely be stored on a regular file 
        # system and passed to os.path.join(). The filename returned 
        # is an ASCII only string for maximum portability.
        # Name the file as teh current time
        timestamp = time.time()
        filename = secure_filename(f"{timestamp}")
        with open(os.path.join(os.environ.get("UPLOAD_FOLDER"), filename), "bw") as f:
            chunk_size = 4096
            while True:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    break

                f.write(chunk)

        # saves file to folder path directory (currently in my computer) 
        # where it'll be accessed to be analyzed. From here on, I'll be 
        # using filename (not 'file') when calling analyze.py

        # app doesn't work here - why?
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #
        #file.save(os.path.join(os.environ.get("UPLOAD_FOLDER"), filename))

        # Now that uploading folder works, call birdnet to analyze
        # python3 analyze.py --i uploads/new_recording_268.m4a  --o outputs --lat 47.613 --lon -122.342

        BIRDNET_FOLDER = 'cd ../BirdNET/' # move to the right folder
        ACTIVATE_VENV = 'source venv/bin/activate' # activate_venv 
        bird_net_run = f'python3 analyze.py --i uploads/{filename} --o outputs --lat {lat} --lon {lon}'
        
        # THIS DOESN'T WORK 
        # 
        # os.system(BIRDNET_FOLDER)
        # # activate_venv 
        # os.system(ACTIVATE_VENV)
        # call birdnet with command line stuff birdnet processes it 
        # os.system(bird_net_run)
        
        # join all the elements so it looks like this because it doesn't
        # work
        bird_net_run = os.system(f'{BIRDNET_FOLDER} && {ACTIVATE_VENV} && {bird_net_run}')

        # Add parsing of file here - using json module - (in parse_txt_file_json.py)
        results_json = parse_output_file(get_file_name(filename))

        # this return is just to double check that file is being handled
        # now return also includes the whole process of parsing text file
        # outputed by BirdNET into a JSON object
        return jsonify(results_json), 200 
        
        # ADD 400 RESPONSE!
        
    # this is where my swift integration  has to go I think?           
    # get from swift client, default is 1
    return'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        <br><br>
        <label for="latitude">Enter latitude:</label>
        <input id="latitude" name="lat" type="number" min="-90.000000" max="90.000000" step="0.000001"><br><br>
        <label for="longitude">Enter longitude:</label>
        <input id="longitude" name="lon" type="number" min="-180.000000" max="180.000000" step="0.000001"><br><br>
        </form>
    '''

# BIRD - ROUTE - route function receives a file, lat, lon inputs from 
# client. It runs birdnet and returns a result
#####################################################################
@bird_bp.route("/bird", methods=['GET', 'POST'], strict_slashes=False)
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url) # redirect to where request was sent from
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url) # SEND HOME TRY AGAIN

        # here add latitude and longitude upload
        if 'lat' not in request.files and 'lon' not in request.files:
            lat, lon = 1, 1
        else:
            lat = request.files['lat']
            lon = request.files['lon']
        # file exists and it has the correct extension    
        if file and allowed_file(file.filename):
            # secure_filename returns a secure version of it, then the 
            # file(now 'filename') can safely be stored on a regular file 
            # system and passed to os.path.join(). The filename returned 
            # is an ASCII only string for maximum portability.
            filename = secure_filename(file.filename)
            # saves file to folder path directory (currently in my computer) 
            # where it'll be accessed to be analyzed. From here on, I'll be 
            # using filename (not 'file') when calling analyze.py

            # app doesn't work here - why?
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            #
            file.save(os.path.join(os.environ.get("UPLOAD_FOLDER"), filename))

            # Now that uploading folder works, call birdnet to analyze
            # python3 analyze.py --i uploads/new_recording_268.m4a  --o outputs --lat 47.613 --lon -122.342

            BIRDNET_FOLDER = 'cd ../BirdNET/' # move to the right folder
            ACTIVATE_VENV = 'source venv/bin/activate' # activate_venv 
            bird_net_run = f'python3 analyze.py --i uploads/{filename} --o outputs --lat {lat} --lon {lon}'
            
            # THIS DOESN'T WORK 
            # 
            # os.system(BIRDNET_FOLDER)
            # # activate_venv 
            # os.system(ACTIVATE_VENV)
            # call birdnet with command line stuff birdnet processes it 
            # os.system(bird_net_run)
            
            # join all the elements so it looks like this because it doesn't
            # work
            bird_net_run = os.system(f'{BIRDNET_FOLDER} && {ACTIVATE_VENV} && {bird_net_run}')

            # Add parsing of file here - using json module - (in parse_txt_file_json.py)
            results_json = parse_output_file(get_file_name(filename))

            # this return is just to double check that file is being handled
            # now return also includes the whole process of parsing text file
            # outputed by BirdNET into a JSON object
            return jsonify(results_json), 200 
            
            # ADD 400 RESPONSE!
            
    # this is where my swift integration  has to go I think?           
    # get from swift client, default is 1
    return'''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        <br><br>
        <label for="latitude">Enter latitude:</label>
        <input id="latitude" name="lat" type="number" min="-90.000000" max="90.000000" step="0.000001"><br><br>
        <label for="longitude">Enter longitude:</label>
        <input id="longitude" name="lon" type="number" min="-180.000000" max="180.000000" step="0.000001"><br><br>
        </form>
    '''

# # STRETCH 
# ########################################################################
# # collections_bp = Blueprint("collections", __name__, url_prefix="/collections")
# # 
# ################################################################


