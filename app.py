import pymongo
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run()


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
def search_songs():
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

    db.collection_name.update_one( {
        { "user_name": user_name, "song_name": song_name  },
        {
            "$set":{
                "user_name": updated_user_name
                "song_name": updated_song_name
            }
        }
    })




# Connecting to local host
connection = pymongo.MongoClient("mongodb://localhost:27017")
db = connection["test_database"]
