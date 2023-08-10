from fastapi import HTTPException
from redis.exceptions import ConnectionError, ResponseError
from urllib.parse import urlencode
import os


def check_env_var(env_var_name: str, default=None) -> str:
    env_var = os.getenv(env_var_name, default)
    if not env_var:
        raise ValueError(
            f'{env_var_name} is not properly set for the environment')
    return env_var


def generate_auth_url(
        auth_url,
        client_id,
        SCOPE,
        state,
        SERVICE,
        extra_params={}
):
    redirect_uri = check_env_var(
        f'{SERVICE}_REDIRECT_URI',
        'http://localhost:3000'
    )
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


def store_refreshed_tokens(
    redis,
    service,
    old_jwt: str,
    new_jwt: str,
    service_name: str
) -> None:
    refresh_token = get_redis_value(
        redis,
        f'{old_jwt}_{service_name}_refresh_token'
    )
    if refresh_token is not None:
        refresh_token = refresh_token.decode('utf-8')
        new_access_token = service.refresh_access_token()
        if new_access_token is not None:
            set_redis(
                redis,
                f'{new_jwt}_{service_name}_access_token',
                new_access_token,
                3600
            )
            delete_redis(
                redis,
                f'{old_jwt}_{service_name}_access_token'
            )
            set_redis(
                redis,
                f'{new_jwt}_{service_name}_access_token',
                refresh_token,
                3600
            )
            delete_redis(
                redis,
                f'{old_jwt}_{service_name}_refresh_token'
            )
            return f'{service_name} session refreshed'
        return f'{service_name} session failed to refresh'


def handle_redis_exceptions(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ConnectionError:
            raise HTTPException(
                status_code=503,
                detail='Service Unavailable: Unable to connect to Redis.'
            )
        except ResponseError:
            raise HTTPException(
                status_code=503,
                detail='Internal Server Error: Unexpected response from Redis.'
            )
    return wrap


@handle_redis_exceptions
def set_redis(redis, key: str, value: str, expiry_time: int):
    redis.set(key, value, ex=expiry_time)


@handle_redis_exceptions
def get_redis_value(redis, key: str):
    return redis.get(key)


@handle_redis_exceptions
def delete_redis(redis, key: str):
    redis.delete(key)
