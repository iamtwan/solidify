from fastapi import APIRouter, Depends, Request
from ..utils.auth import generate_auth_url, check_env_var
from ..utils.jwt import create_access_token
from ..services.auth import process_oauth_callback
from ..dependencies import get_redis, get_current_user_jwt
from datetime import timedelta
import uuid


SCOPE = 'playlist-read-private'
SHOW_DIALOG = 'false'
SERVICE = 'spotify'

router = APIRouter()


@router.get('/spotify/login')
def login(request: Request, redis=Depends(get_redis)):
    client_id = check_env_var('SPOTIFY_CLIENT_ID')
    jw_token = get_current_user_jwt(request)
    if not jw_token:
        jw_token = create_access_token(
            subject=str(uuid.uuid4()),
            expires_delta=timedelta(hours=1)
        )
    state = jw_token
    redis.set(f'{state}_spotify_state', 'valid', ex=600)
    auth_url = generate_auth_url(
        'https://accounts.spotify.com/authorize',
        client_id,
        SCOPE,
        state,
        SERVICE,
        {'show_dialog': SHOW_DIALOG}
    )
    return {'url': auth_url, 'jw_token': jw_token}


@router.get('/spotify/callback')
def callback(code: str, state: str, redis=Depends(get_redis)):
    token_url = 'https://accounts.spotify.com/api/token'
    return process_oauth_callback(
        code,
        state,
        SERVICE,
        token_url,
        check_env_var('SPOTIFY_CLIENT_ID'),
        check_env_var('SPOTIFY_CLIENT_SECRET'),
        redis
    )
