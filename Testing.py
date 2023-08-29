import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, session, request, redirect
from flask_session import Session



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

def main():

    @app.route('/')
    def index():

        cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                                cache_handler=cache_handler,
                                                show_dialog=True)

        if request.args.get("code"):
            # Step 2. Being redirected from Spotify auth page
            auth_manager.get_access_token(request.args.get("code"))
            return redirect('/')

        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            # Step 1. Display sign in link when no token
            auth_url = auth_manager.get_authorize_url()
            return f'<h2><a href="{auth_url}">Sign in</a></h2>'

        # Step 3. Signed in, display data
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return f'<h2>Hi {spotify.me()["display_name"]}, ' \
            f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
            f'<a href="/playlists">my playlists</a> | ' \
            f'<a href="/currently_playing">currently playing</a> | ' \
            f'<a href="/current_user">me</a>' \



    @app.route('/sign_out')
    def sign_out():
        session.pop("token_info", None)
        return redirect('/')
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


