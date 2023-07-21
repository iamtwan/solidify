from fastapi import APIRouter, Depends
from ..dependencies import get_spotify_service
from ..services.spotify import SpotifyService


router = APIRouter()

@router.get('/{playlist_id}')
def read_playlist(playlist_id: str, spotify_service: SpotifyService = Depends(get_spotify_service)):
    playlist = spotify_service.get_playlist(playlist_id)
    return playlist
