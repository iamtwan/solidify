import os
from .services.spotify import SpotifyService


def get_spotify_service():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    return SpotifyService(client_id, client_secret)
