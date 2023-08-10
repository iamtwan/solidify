from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_user_google_service, get_redis, user_google_refresh, get_current_user_jwt
from ..utils.jwt import create_access_token
from ..utils.auth import store_refreshed_tokens, get_redis_value
from ..services.google import GoogleService
from datetime import timedelta


router = APIRouter()


@router.post('/upload/{playlist_id}', tags=['Google'])
def upload_to_google(
    playlist_id: str,
    google_service: GoogleService = Depends(get_user_google_service)
):
    redis = get_redis()
    csv_content_raw = get_redis_value(redis, f'{playlist_id}_csv')
    if csv_content_raw is None:
        raise HTTPException(
            status_code=404,
            detail='Cannot locate CSV key in Redis'
        )
    csv_content = csv_content_raw.decode('utf-8')

    status, response = google_service.upload_file(
        playlist_id,
        csv_content
    )
    if status == 200:
        return {'status': 'File successfully uploaded'}
    else:
        raise HTTPException(
            status_code=status,
            detail=f'Google Drive API responded with status: {status}. Response: {response}'
        )


@router.post('/refresh', tags=['Google'])
async def refresh_google_session(
    redis=Depends(get_redis),
    old_jwt=Depends(get_current_user_jwt),
    google_service: GoogleService = Depends(user_google_refresh)
):
    if google_service is None:
        raise HTTPException(
            status_code=400,
            detail='Spotify not connected or redis cannot locate jwt'
        )

    new_jwt = create_access_token(
        subject=old_jwt,
        expires_delta=timedelta(hours=1)
    )

    google_status = store_refreshed_tokens(
        redis,
        google_service,
        old_jwt,
        new_jwt,
        'GOOGLE'
    )

    if google_status is None:
        raise HTTPException(
            status_code=400, detail='Failed to refresh Google session')

    return {
        'google_status': google_status,
        'new_jwt': new_jwt,
    }
