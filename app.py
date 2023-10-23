import pymongo
from flask import Flask, request, render_template, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
import os

import pymongo
import datetime
from bson.objectid import ObjectId
import sys



app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv()  # take environment variables from .env.

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# connect to the database
# cxn = pymongo.MongoClient(os.getenv("mongodb+srv://last-team:<password>@cluster0.m5t5gvu.mongodb.net/?retryWrites=true&w=majority"), serverSelectionTimeoutMS=5000)
# try:
#     # verify the connection works by pinging the database
#     cxn.admin.command('ping') # The ping command is cheap and does not require auth.
#     db = cxn[os.getenv('music_app')] # store a reference to the database
#     print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
# except Exception as e:
#     # the ping command failed, so the connection is not available.
#     print(' *', "Failed to connect to MongoDB at", os.getenv("mongodb+srv://last-team:<password>@cluster0.m5t5gvu.mongodb.net/?retryWrites=true&w=majority"))
#     print('Database connection error:', e) # debug


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

mycol = mydb["mycollection"]


# Views
@app.route("/")
@app.route("/<user_name>")
def display_songs(user_name=None):
    song_list = None
    if user_name:
        song_list = db.collection.find({"user_name": user_name})
    else:
        song_list = db.collection.find({})

    return render_template("home.html", song_list=song_list)


@app.route("/add-songs")
def add_songs():
    return render_template("addSongs.html")


@app.route("/delete-songs")
def delete_songs():
    return render_template("deleteSongs.html")


@app.route("/search-songs")
def search_songs():
    return render_template("searchSongs.html")


@app.route("/edit-songs")
def edit_songs():
    return render_template("editSongs.html")


# Form methods
@app.route("/api/add-songs", methods=["POST"])
def addSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    db.collection.insert_one({"user_name": user_name, "song_name": song_name})
    return redirect("/")


@app.route("/api/delete-songs", methods=["POST"])
def deleteSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    db.collection.delete_one({"user_name": user_name, "song_name": song_name})
    return redirect("/")


@app.route("/api/search-songs", methods=["POST"])
def searchSongs():
    user_name = request.form["user_name"]
    return redirect("/" + user_name)


@app.route("/api/edit-songs", methods=["POST"])
def editSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    updated_user_name = request.form["updated_user_name"]
    updated_song_name = request.form["updated_song_name"]

    db.collection.update_one(
        {"user_name": user_name, "song_name": song_name},
        {"$set": {"user_name": updated_user_name, "song_name": updated_song_name}},
    )
    return redirect("/")



if __name__ == "__main__":
    app.debug = True
    PORT = os.getenv('PORT', 5000) # use the PORT environment variable, or default to 5000

    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=PORT)


# Connecting to local host
# connection = pymongo.MongoClient("mongodb://localhost:27017")
# db = connection["test_database"]
