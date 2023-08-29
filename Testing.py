import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")  # Set your own secret key

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

# Initialize Spotipy with OAuth2
sp_oauth = SpotifyOAuth(
    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope="playlist-modify-private"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect(url_for("create_playlist"))

@app.route("/create_playlist")
def create_playlist():
    if "token_info" not in session:
        return redirect(url_for("login"))

    token_info = session["token_info"]
    sp = spotipy.Spotify(auth=token_info["access_token"])

    user_info = sp.me()
    user_id = user_info["id"]

    playlist_name = "My Awesome Playlist"
    playlist_description = "Created with my cool app!"

    playlist = sp.user_playlist_create(
        user_id, playlist_name, public=False, description=playlist_description
    )

    return f"Playlist created! Name: {playlist_name}, ID: {playlist['id']}"

if __name__ == "__main__":
    app.run(debug=True)
