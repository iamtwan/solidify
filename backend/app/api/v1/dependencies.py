import os
import redis
from .services.spotify import SpotifyService
from fastapi import HTTPException, status, Depends, Request
from jose import jwt, JWTError


ALGORITHM = 'HS256'


def get_redis():
    return redis.Redis(host='redis', port=6379, db=0)


def get_spotify_service():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    return SpotifyService(client_id, client_secret)


def get_current_user_id(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header is missing',
        )
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authorization scheme',
            )

        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise ValueError('SECRET_KEY is not set in the environment')
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        subject = payload.get('sub')

        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token, subject is missing'
            )

        return subject

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired jw_token',
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authorization header',
        )


def get_user_spotify_service(
        user_id: str = Depends(get_current_user_id),
        redis=Depends(get_redis)
):
    access_token_raw = redis.get(f'{user_id}_access_token')
    refresh_token_raw = redis.get(f'{user_id}_refresh_token')

    if access_token_raw is None or refresh_token_raw is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
        )

    access_token = access_token_raw.decode('utf-8')
    refresh_token = refresh_token_raw.decode('utf-8')

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    return SpotifyService(
        client_id,
        client_secret,
        access_token,
        refresh_token
    )
