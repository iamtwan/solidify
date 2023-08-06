from fastapi import APIRouter, Depends, Request
from ..utils.auth import generate_auth_url, check_env_var
from ..dependencies import get_redis, get_current_user_jwt
from ..utils.jwt import create_access_token
from ..services.auth import process_oauth_callback
from datetime import timedelta
import uuid


SCOPE = 'https://www.googleapis.com/auth/drive.file'
SERVICE = 'google'

router = APIRouter()


@router.get('/google/login', tags=['Authorization'])
def login(request: Request, redis=Depends(get_redis)):
    client_id = check_env_var('GOOGLE_CLIENT_ID')
    jw_token = get_current_user_jwt(request)
    if not jw_token:
        jw_token = create_access_token(
            subject=str(uuid.uuid4()),
            expires_delta=timedelta(hours=1)
        )
    state = jw_token
    redis.set(f'{state}_google_state', 'valid', ex=600)

    auth_url = generate_auth_url(
        'https://accounts.google.com/o/oauth2/v2/auth',
        client_id,
        SCOPE,
        state,
        SERVICE,
        {'access_type': 'offline', 'prompt': 'consent'}
    )
    return {'url': auth_url, 'jw_token': jw_token}


@router.get('/google/callback', tags=['Authorization'])
def callback(code: str, state: str, redis=Depends(get_redis)):
    token_url = 'https://oauth2.googleapis.com/token'
    return process_oauth_callback(
        code,
        state,
        SERVICE,
        token_url,
        check_env_var('GOOGLE_CLIENT_ID'),
        check_env_var('GOOGLE_CLIENT_SECRET'),
        redis
    )
