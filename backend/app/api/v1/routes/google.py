from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_user_google_service, get_redis
from ..services.google import GoogleService


router = APIRouter()


@router.post('/upload/{playlist_id}')
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
