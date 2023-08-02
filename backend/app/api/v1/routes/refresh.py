from fastapi import APIRouter, Depends, HTTPException
from ..services.spotify import SpotifyService
from ..services.google import GoogleService
from ..dependencies import get_redis, get_current_user_jwt, user_spotify_refresh, user_google_refresh
from ..utils.jwt import create_access_token
from ..utils.auth import store_refreshed_tokens
from datetime import timedelta


router = APIRouter()


@router.post('/refresh', tags=['Authorization'])
async def refresh_user_session(
    redis=Depends(get_redis),
    old_jwt=Depends(get_current_user_jwt),
    spotify_service: SpotifyService = Depends(user_spotify_refresh),
    google_service: GoogleService = Depends(user_google_refresh)
):
    new_jwt = create_access_token(
        subject=old_jwt,
        expires_delta=timedelta(hours=1)
    )
    try:
        store_refreshed_tokens(
            redis,
            spotify_service,
            old_jwt,
            new_jwt,
            'spotify'
        )
        store_refreshed_tokens(
            redis,
            google_service,
            old_jwt,
            new_jwt,
            'google'
        )

        return {'status': 'Session refreshed', 'new jwt': new_jwt}

    except HTTPException:
        raise
