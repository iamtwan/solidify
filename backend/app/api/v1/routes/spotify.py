from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_spotify_service, get_user_spotify_service
from ..services.spotify import SpotifyService
from requests.exceptions import HTTPError


router = APIRouter()


@router.get('/all', tags=['Spotify'])
def get_all_playlists(
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    all_playlists = spotify_service.get_all_playlists()
    return all_playlists


@router.get('/private/{playlist_id}', tags=['Spotify'])
def get_protected_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    playlist = spotify_service.get_protected_playlist(playlist_id)
    return playlist


@router.get('/{playlist_id}', tags=['Spotify'])
def get_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_spotify_service)
):
    playlist = spotify_service.get_playlist(playlist_id)
    return playlist


@router.get('/user', tags=['Spotify'])
def check_token_validity(
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    try:
        spotify_service.get_user_profile()
        return {'valid token': True}
    except HTTPError as error:
        if error.response.status_code == 401:
            return {'valid token': False}
        else:
            raise HTTPException(
                status_code=500,
                detail='Unexpected error while checking token validity',
            )
