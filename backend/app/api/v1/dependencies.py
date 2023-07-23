import os
import redis
from .services.spotify import SpotifyService
from fastapi import HTTPException, status, Depends


def get_redis():
    return redis.Redis(host='localhost', port=6379, db=0)


def get_spotify_service():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    return SpotifyService(client_id, client_secret)


def get_user_spotify_service(redis=Depends(get_redis)):
    access_token = redis.get('access_token')
    refresh_token = redis.get('refresh_token')
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
        )
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    return SpotifyService(client_id, client_secret, access_token, refresh_token)
