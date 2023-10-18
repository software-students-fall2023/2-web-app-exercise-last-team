import pymongo
from flask import Flask, request

app = Flask(__name__)


# Views
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Form methods
@app.route("/api/add-songs", methods=["POST"])
def addSongs():
    user = request.form["user"]
    song_name = request.form["song_name"]
    db.songs.insert_one({"user": user, "song_name": song_name})


@app.route("/api/delete-songs", methods=["POST"])
def deleteSongs():
    user = request.form["user"]
    song_name = request.form["song_name"]
    db.songs.delete_one({"user": user, "song_name": song_name})


# Connecting to local host
connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection
