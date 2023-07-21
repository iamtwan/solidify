from .services.spotify import SpotifyService


def get_spotify_service():
    client_id = 'client_id'
    client_secret = 'client_secret'
    return SpotifyService(client_id, client_secret)
