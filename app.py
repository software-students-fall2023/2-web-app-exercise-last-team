import pymongo
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


# Views
@app.route("/")
@app.route("/<user_name>")
def hello_world(user_name=None):
    song_list = None
    if user_name:
        song_list = db.songs.find({"user_name": user_name})
    else:
        song_list = db.songs.find({})

    return render_template("home.html", song_list=song_list)


# Form methods
@app.route("/api/add-songs", methods=["POST"])
def addSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    db.songs.insert_one({"user_name": user_name, "song_name": song_name})
    return redirect("/")


@app.route("/api/delete-songs", methods=["POST"])
def deleteSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    db.songs.delete_one({"user_name": user_name, "song_name": song_name})
    return redirect("/")


# Connecting to local host
connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["test_database"]
