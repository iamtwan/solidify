from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_spotify_service, get_user_spotify_service, user_spotify_refresh, get_redis, get_current_user_jwt
from ..utils.jwt import create_access_token
from ..utils.auth import store_refreshed_tokens
from ..services.spotify import SpotifyService
from requests.exceptions import HTTPError
from ..models.spotify import AllPlaylistsResponse, Playlist, TokenValidity
from ..models.auth import RefreshTokens
from datetime import timedelta


router = APIRouter()


@router.get('/playlists/all', response_model=AllPlaylistsResponse, tags=['Spotify'])
def get_all_playlists(
    offset: int = 0,
    limit: int = 1,
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    all_playlists, next_link = spotify_service.get_all_playlists(offset, limit)
    return AllPlaylistsResponse(playlists=all_playlists, next=next_link)


@router.get('/playlists/private/{playlist_id}', response_model=Playlist, tags=['Spotify'])
def get_protected_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    playlist = spotify_service.get_protected_playlist(playlist_id)
    return playlist


@router.get('/playlists/{playlist_id}', response_model=Playlist, tags=['Spotify'])
def get_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_spotify_service)
):
    playlist = spotify_service.get_playlist(playlist_id)
    return playlist


@router.get('/user', response_model=TokenValidity, tags=['Spotify'])
def check_token_validity(
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    try:
        spotify_service.get_user_profile()
        return TokenValidity(user_spotify_token=True)
    except HTTPError as error:
        if error.response.status_code == 401:
            return TokenValidity(user_spotify_token=False)
        else:
            raise HTTPException(
                status_code=500,
                detail='Unexpected error while checking token validity',
            )


@router.post('/refresh', response_model=RefreshTokens, tags=['Spotify'])
async def refresh_spotify_session(
    redis=Depends(get_redis),
    old_jwt=Depends(get_current_user_jwt),
    spotify_service: SpotifyService = Depends(user_spotify_refresh)
):
    if spotify_service is None:
        raise HTTPException(
            status_code=400,
            detail='Spotify not connected or redis cannot locate jwt'
        )

    new_jwt = create_access_token(
        subject=old_jwt,
        expires_delta=timedelta(hours=1)
    )

    spotify_status = store_refreshed_tokens(
        redis,
        spotify_service,
        old_jwt,
        new_jwt,
        'SPOTIFY'
    )

    if spotify_status is None:
        raise HTTPException(
            status_code=400, detail='Failed to refresh Spotify session')

    return {
        'service_status': spotify_status,
        'new_jwt': new_jwt
    }
