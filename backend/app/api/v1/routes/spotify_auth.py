from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import RedirectResponse
from ..utils.jwt import create_access_token
from ..dependencies import get_redis
from urllib.parse import urlencode
import requests
import os


SCOPE = 'playlist-read-private'
# need to generate a proper state for deployment
STATE = 'random-pass'
SHOW_DIALOG = 'false'

router = APIRouter()


def check_env_var(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if not env_var:
        raise ValueError(f'{env_var_name} is not set in the environment')
    return env_var


@router.get('/login')
def login():
    client_id = check_env_var('CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:8000/v1/auth/callback')
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': SCOPE,
        'state': STATE,
        'show_dialog': SHOW_DIALOG,
    }
    url = f'{auth_url}?{urlencode(params)}'
    return RedirectResponse(url)


@router.get('/callback')
def callback(code: str, state: str, redis=Depends(get_redis)):
    try:
        if state != STATE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='State mismatch',
            )

        client_id = check_env_var('CLIENT_ID')
        client_secret = check_env_var('CLIENT_SECRET')
        if not client_secret:
            raise ValueError('CLIENT_SECRET is not set in the environment')
        redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:8000/v1/auth/callback')

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

        redis.set('access_token', tokens['access_token'])
        redis.set('refresh_token', tokens['refresh_token'])

        # TODO: Replace 'spotify_user_id' with the actual user ID
        access_token = create_access_token(subject='spotify_user_id')
        return {'access_token': access_token}

    except HTTPException as exception:
        return exception
