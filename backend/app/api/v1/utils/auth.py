from fastapi import HTTPException, status
from urllib.parse import urlencode
import requests
import os
import traceback


def check_env_var(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if not env_var:
        raise ValueError(f'{env_var_name} is not set in the environment')
    return env_var


def generate_auth_url(
        auth_url,
        client_id,
        SCOPE,
        state,
        extra_params={}
):
    redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:3000')
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': SCOPE,
        'state': state,
    }
    params.update(extra_params)
    url = f'{auth_url}?{urlencode(params)}'
    return url


def process_oauth_callback(
        code,
        state,
        service,
        token_url,
        client_id,
        client_secret,
        redis
):
    redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:3000')
    try:
        valid = redis.get(f'{state}_{service}_state')
        if valid:
            valid = valid.decode('utf-8')
        print('Valid variable:', valid)
        if not valid or valid != 'valid':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='State mismatch'
            )
        jw_token = state
        redis.delete(f'{state}_{service}_state')

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()

        tokens = response.json()

        expiry_time = tokens['expires_in']

        redis.set(
            f'{jw_token}_{service}_access_token',
            tokens['access_token'],
            ex=expiry_time
        )
        redis.set(
            f'{jw_token}_{service}_refresh_token',
            tokens['refresh_token'],
            ex=expiry_time
        )

        return {'status': f'{service} successfully connected'}

    except requests.exceptions.RequestException as exception:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )

    except Exception as exception:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exception)
        )
