import pymongo
from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)

# Connecting to local host
# connection = pymongo.MongoClient("mongodb://localhost:27017")
# db = connection["test_database"]

# connect to the database
password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

connection = pymongo.MongoClient(
    os.getenv(
        "mongodb+srv://last-team:"
        + str(password)
        + "@cluster0.m5t5gvu.mongodb.net/?retryWrites=true&w=majority"
    ),
    serverSelectionTimeoutMS=5000,
)
try:
    db = connection["music_app"]
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(
        " *",
        "Failed to connect to MongoDB at",
        os.getenv(
            "mongodb+srv://last-team:"
            + str(password)
            + "@cluster0.m5t5gvu.mongodb.net/?retryWrites=true&w=majority"
        ),
    )
    print("Database connection error:", e)  # debug


# Views
@app.route("/")
@app.route("/<user_name>")
def display_songs(user_name=None):
    song_list = None
    if user_name:
        song_list = db.songs.find({"user_name": user_name})
    else:
        song_list = db.songs.find({})

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
    db.songs.insert_one({"user_name": user_name, "song_name": song_name})
    return redirect("/")


@app.route("/api/delete-songs", methods=["POST"])
def deleteSongs():
    user_name = request.form["user_name"]
    song_name = request.form["song_name"]
    db.songs.delete_one({"user_name": user_name, "song_name": song_name})
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

    db.songs.update_one(
        {"user_name": user_name, "song_name": song_name},
        {"$set": {"user_name": updated_user_name, "song_name": updated_song_name}},
    )
    return redirect("/")


if __name__ == "__main__":
    PORT = os.getenv(
        "PORT", 5000
    )  # use the PORT environment variable, or default to 5000

    # import logging
    # logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(port=PORT)
