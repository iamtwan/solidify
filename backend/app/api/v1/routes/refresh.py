from fastapi import APIRouter, Depends, HTTPException
from ..services.spotify import SpotifyService
from ..services.google import GoogleService
from ..dependencies import get_redis, get_current_user_jwt, user_spotify_service_refresh, user_google_service_refresh
from ..utils.jwt import create_access_token
from datetime import timedelta


router = APIRouter()


@router.post('/refresh', tags=['Authorization'])
async def refresh_user_session(
    redis=Depends(get_redis),
    old_jwt=Depends(get_current_user_jwt),
    spotify_service: SpotifyService = Depends(
        user_spotify_service_refresh),
    google_service: GoogleService = Depends(
        user_google_service_refresh)
):
    new_jw_token = create_access_token(
        subject=old_jwt,
        expires_delta=timedelta(hours=1)
    )
    try:
        spotify_refresh_token = redis.get(
            f'{old_jwt}_spotify_refresh_token').decode('utf-8')
        if spotify_refresh_token is not None:
            new_access_token = spotify_service.refresh_access_token()
            if new_access_token is not None:
                redis.set(
                    f'{new_jw_token}_spotify_access_token',
                    new_access_token, ex=3600
                )
                redis.set(
                    f'{new_jw_token}_spotify_refresh_token',
                    spotify_refresh_token, ex=3600
                )

        google_refresh_token = redis.get(
            f'{old_jwt}_google_refresh_token').decode('utf-8')
        if google_refresh_token is not None:
            new_access_token = google_service.refresh_access_token()
            if new_access_token is not None:
                redis.set(
                    f'{new_jw_token}_google_access_token',
                    new_access_token, ex=3600
                )
                redis.set(
                    f'{new_jw_token}_google_refresh_token',
                    google_refresh_token, ex=3600
                )

        return {'status': 'Session refreshed', 'new jwt': new_jw_token}

    except HTTPException:
        raise
