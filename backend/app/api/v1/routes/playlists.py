from fastapi import APIRouter, Depends
from ..dependencies import get_spotify_service, get_user_spotify_service
from ..services.spotify import SpotifyService


router = APIRouter()


@router.get('/{playlist_id}')
def get_playlist(playlist_id: str, spotify_service: SpotifyService = Depends(get_spotify_service)):
    playlist = spotify_service.get_playlist(playlist_id)
    return playlist


@router.get('/all_playlists')
def get_all_protected_playlists(spotify_service: SpotifyService = Depends(get_user_spotify_service)):
    playlists = spotify_service.get_protected_playlists()
    return playlists
