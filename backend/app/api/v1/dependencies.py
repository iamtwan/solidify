from fastapi import HTTPException, status, Depends, Request
from .utils.auth import check_env_var
from .services.redis import RedisHandler
import redis


REDIS_HOST = check_env_var('REDIS_HOST', 'redis')
REDIS_PORT = int(check_env_var('REDIS_PORT', '6379'))
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)


def get_redis():
    return redis.Redis(connection_pool=pool)


def get_spotify_service():
    from .services.spotify import SpotifyService
    client_id = check_env_var('SPOTIFY_CLIENT_ID')
    client_secret = check_env_var('SPOTIFY_CLIENT_SECRET')
    return SpotifyService(client_id, client_secret)


def get_current_user_jwt(request: Request, raise_error: bool = True):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        if raise_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Missing authorization header',
            )
        return None

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authorization scheme, expected: Bearer',
            )

        return token

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authorization header, expected: Bearer Token',
        )


def get_user_service(service, jw_token: str, redis, refresh: bool = False):
    from .services.spotify import SpotifyService
    from .services.google import GoogleService

    services = {
        'SPOTIFY': {
            'service': SpotifyService,
            'client_id': check_env_var('SPOTIFY_CLIENT_ID'),
            'client_secret': check_env_var('SPOTIFY_CLIENT_SECRET')
        },
        'GOOGLE': {
            'service': GoogleService,
            'client_id': check_env_var('GOOGLE_CLIENT_ID'),
            'client_secret': check_env_var('GOOGLE_CLIENT_SECRET')
        }
    }

    assert service in services, f'Service {service} not supported'

    service_data = services[service]
    service_class = service_data['service']
    redis_handler = RedisHandler()

    access_token_raw = redis_handler.get_redis_value(
        redis, f'{jw_token}_{service}_access_token')
    refresh_token_raw = redis_handler.get_redis_value(
        redis, f'{jw_token}_{service}_refresh_token')

    if access_token_raw is None or refresh_token_raw is None:
        if refresh:
            return None
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'JWT cannot be located in Redis. User may not be authenticated for {service}'
            )

    access_token = access_token_raw.decode('utf-8')
    refresh_token = refresh_token_raw.decode('utf-8')
    client_id = service_data['client_id']
    client_secret = service_data['client_secret']

    return service_class(
        client_id,
        client_secret,
        access_token,
        refresh_token
    )


def get_user_spotify_service(
    jw_token: str = Depends(get_current_user_jwt),
    redis=Depends(get_redis)
):
    return get_user_service('SPOTIFY', jw_token, redis)


def user_spotify_refresh(
    jw_token: str = Depends(get_current_user_jwt),
    redis=Depends(get_redis)
):
    return get_user_service('SPOTIFY', jw_token, redis, refresh=True)


def get_user_google_service(
    jw_token: str = Depends(get_current_user_jwt),
    redis=Depends(get_redis)
):
    return get_user_service('GOOGLE', jw_token, redis)


def user_google_refresh(
    jw_token: str = Depends(get_current_user_jwt),
    redis=Depends(get_redis)
):
    return get_user_service('GOOGLE', jw_token, redis, refresh=True)
