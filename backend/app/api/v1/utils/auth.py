from urllib.parse import urlencode
import os


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
