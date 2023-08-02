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
    redirect_uri = os.getenv(
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
    if service is None:
        print(f'No {service_name} service connected')
        return
    refresh_token = redis.get(f'{old_jwt}_{service_name}_refresh_token')
    if refresh_token is not None:
        refresh_token = refresh_token.decode('utf-8')
        new_access_token = service.refresh_access_token()
        if new_access_token is not None:
            redis.set(
                f'{new_jwt}_{service_name}_access_token',
                new_access_token, ex=3600
            )
            redis.delete(f'{old_jwt}_{service_name}_access_token')
            redis.set(
                f'{new_jwt}_{service_name}_refresh_token',
                refresh_token, ex=3600
            )
            redis.delete(f'{old_jwt}_{service_name}_refresh_token')
