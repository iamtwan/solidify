from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import RedirectResponse
from ..utils.jwt import create_access_token
from ..dependencies import get_redis
from urllib.parse import urlencode
from datetime import timedelta
import requests
import os
import uuid


SCOPE = 'playlist-read-private'
SHOW_DIALOG = 'false'

router = APIRouter()


def check_env_var(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if not env_var:
        raise ValueError(f'{env_var_name} is not set in the environment')
    return env_var


@router.get('/login')
def login(redis=Depends(get_redis)):
    client_id = check_env_var('CLIENT_ID')
    redirect_uri = os.getenv(
        'REDIRECT_URI', 'http://localhost:8000/v1/auth/callback')
    auth_url = 'https://accounts.spotify.com/authorize'
    state = str(uuid.uuid4())
    redis.set(f'{state}_state', 'valid', ex=1800)
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': SCOPE,
        'state': state,
        'show_dialog': SHOW_DIALOG,
    }
    url = f'{auth_url}?{urlencode(params)}'
    return RedirectResponse(url)


@router.get('/callback')
def callback(code: str, state: str, redis=Depends(get_redis)):
    try:
        valid = redis.get(f'{state}_state')
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='State mismatch',
            )
        redis.delete(f'{state}_state')

        client_id = check_env_var('CLIENT_ID')
        client_secret = check_env_var('CLIENT_SECRET')
        if not client_secret:
            raise ValueError('CLIENT_SECRET is not set in the environment')
        redirect_uri = os.getenv(
            'REDIRECT_URI', 'http://localhost:8000/v1/auth/callback')

        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()

        tokens = response.json()

        random_id = str(uuid.uuid4())
        expiry_time = tokens['expires_in'] - (5 * 60)

        redis.set(
            f'{random_id}_access_token',
            tokens['access_token'],
            ex=expiry_time
        )
        redis.set(
            f'{random_id}refresh_token',
            tokens['refresh_token'],
            ex=expiry_time
        )

        jw_token = create_access_token(
            subject=random_id,
            expires_delta=timedelta(seconds=expiry_time)
        )
        return {'jw_token': jw_token}

    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exception),
        )
