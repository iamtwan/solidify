from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os


ALGORITHM = 'HS256'


def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None
):
    """
    Creates a JWT access token.

    Parameters:
        subject (str): The subject of the token (typically a user identifier).
        expires_delta (Optional[timedelta]): The lifespan of the token. If not
        provided, the default value will be used (ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns:
        str: The encoded JWT as a string.

    SECRET_KEY:
        You may run 'openssl rand -hex 32' for env var.
    """
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise ValueError('SECRET_KEY is not set in the environment')
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt
