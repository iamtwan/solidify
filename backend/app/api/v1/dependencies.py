import os
import redis
from .services.spotify import SpotifyService
from .services.google import GoogleService
from fastapi import HTTPException, status, Depends, Request


ALGORITHM = 'HS256'


def get_redis():
    return redis.Redis(host='redis', port=6379, db=0)


def get_spotify_service():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    return SpotifyService(client_id, client_secret)


def get_current_user_jwt(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authorization scheme',
            )

        return token

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authorization header',
        )


def get_user_spotify_service(
        jw_token: str = Depends(get_current_user_jwt),
        redis=Depends(get_redis)
):
    access_token_raw = redis.get(f'{jw_token}_spotify_access_token')
    refresh_token_raw = redis.get(f'{jw_token}_spotify_refresh_token')

    if access_token_raw is None or refresh_token_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
        )

    access_token = access_token_raw.decode('utf-8')
    refresh_token = refresh_token_raw.decode('utf-8')

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    return SpotifyService(
        client_id,
        client_secret,
        access_token,
        refresh_token
    )


def get_user_google_service(
        jw_token: str = Depends(get_current_user_jwt),
        redis=Depends(get_redis)
):
    access_token_raw = redis.get(f'{jw_token}_google_access_token')
    refresh_token_raw = redis.get(f'{jw_token}_google_refresh_token')

    if access_token_raw is None or refresh_token_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    access_token = access_token_raw.decode('utf-8')
    refresh_token = refresh_token_raw.decode('utf-8')

    # client_id = os.getenv('GOOGLE_CLIENT_ID')
    # client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    return GoogleService(
        # client_id,
        # client_secret,
        access_token,
        refresh_token
    )
