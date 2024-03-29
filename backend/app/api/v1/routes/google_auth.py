from fastapi import APIRouter, Depends
from ..utils.auth import generate_auth_url, check_env_var
from ..dependencies import get_redis
from ..utils.jwt import create_access_token
from ..services.auth import process_oauth_callback
from ..services.redis import RedisHandler
from ..models.auth import LoginResponse, CallbackResponse
from datetime import timedelta
import uuid


SCOPE = 'https://www.googleapis.com/auth/drive.file'
SERVICE = 'GOOGLE'

router = APIRouter()


@router.get('/google/login', response_model=LoginResponse, tags=['Authorization'])
def login(redis=Depends(get_redis)):
    client_id = check_env_var('GOOGLE_CLIENT_ID')
    state = str(uuid.uuid4())

    redis_handler = RedisHandler()
    redis_handler.set_redis(redis, f'{state}_{SERVICE}_state', 'valid', 600)

    auth_url = generate_auth_url(
        'https://accounts.google.com/o/oauth2/v2/auth',
        client_id,
        SCOPE,
        state,
        SERVICE,
        {'access_type': 'offline', 'prompt': 'consent'}
    )
    return {'url': auth_url}


@router.get('/google/callback', response_model=CallbackResponse, tags=['Authorization'])
def callback(code: str, state: str, redis=Depends(get_redis)):
    token_url = 'https://oauth2.googleapis.com/token'
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
        check_env_var('GOOGLE_CLIENT_ID'),
        check_env_var('GOOGLE_CLIENT_SECRET'),
        redis
    )
