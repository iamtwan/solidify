from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_user_google_service, get_redis, user_google_refresh, get_current_user_jwt
from ..utils.jwt import create_access_token
from ..utils.auth import store_refreshed_tokens
from ..services.google import GoogleService
from datetime import timedelta


router = APIRouter()


@router.post('/upload/{playlist_id}', tags=['Google'])
def upload_to_google(
    playlist_id: str,
    google_service: GoogleService = Depends(get_user_google_service)
):
    try:
        redis = get_redis()
        csv_content = redis.get(f'{playlist_id}_csv').decode('utf-8')
        if not csv_content:
            return {'status': 'No playlist csv in redis'}

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
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=str(exception)
        )


@router.post('/refresh/google', tags=['Google'])
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
            status_code=400, detail="Failed to refresh Google session")

    return {
        'google_status': google_status,
        'new_jwt': new_jwt,
    }
