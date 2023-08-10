from fastapi import APIRouter, Depends
from ..utils.auth import generate_auth_url, check_env_var
from ..utils.jwt import create_access_token
from ..services.auth import process_oauth_callback
from ..dependencies import get_redis
from ..services.redis import RedisHandler
from datetime import timedelta
import uuid


SCOPE = 'playlist-read-private user-read-private'
SHOW_DIALOG = 'false'
SERVICE = 'SPOTIFY'

router = APIRouter()


@router.get('/spotify/login', tags=['Authorization'])
def login(redis=Depends(get_redis)):
    client_id = check_env_var('SPOTIFY_CLIENT_ID')
    state = str(uuid.uuid4())

    redis_handler = RedisHandler()
    redis_handler.set_redis(redis, f'{state}_{SERVICE}_state', 'valid', 600)

    auth_url = generate_auth_url(
        'https://accounts.spotify.com/authorize',
        client_id,
        SCOPE,
        state,
        SERVICE,
        {'show_dialog': SHOW_DIALOG}
    )
    return {'url': auth_url}


@router.get('/spotify/callback', tags=['Authorization'])
def callback(code: str, state: str, redis=Depends(get_redis)):
    token_url = 'https://accounts.spotify.com/api/token'
    jw_token = create_access_token(
        subject=str(uuid.uuid4()),
        expires_delta=timedelta(hours=1)
    )
    return process_oauth_callback(
        jw_token,
        code,
        state,
        SERVICE,
        token_url,
        check_env_var('SPOTIFY_CLIENT_ID'),
        check_env_var('SPOTIFY_CLIENT_SECRET'),
        redis
    )
