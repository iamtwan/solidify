from fastapi import HTTPException, status
from ..utils.auth import check_env_var
from ..services.redis import RedisHandler
import requests
import traceback


def process_oauth_callback(
        jwt,
        code,
        state,
        SERVICE,
        token_url,
        client_id,
        client_secret,
        redis
):
    redirect_uri = check_env_var(
        f'{SERVICE}_REDIRECT_URI',
        'http://localhost:3000'
    )
    try:
        redis_handler = RedisHandler()

        valid = redis_handler.get_redis_value(
            redis, f'{state}_{SERVICE}_state')
        if valid:
            valid = valid.decode('utf-8')
        if not valid or valid != 'valid':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='State mismatch'
            )
        redis_handler.delete_redis(redis, f'{state}_{SERVICE}_state')

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

        redis_handler.set_redis(
            redis,
            f'{jwt}_{SERVICE}_access_token',
            tokens['access_token'],
            expiry_time
        )

        redis_handler.set_redis(
            redis,
            f'{jwt}_{SERVICE}_refresh_token',
            tokens['refresh_token'],
            expiry_time
        )

        return {'status': f'{SERVICE} successfully connected', 'jwt': jwt}

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
