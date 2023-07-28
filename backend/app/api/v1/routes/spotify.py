from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_spotify_service, get_user_spotify_service, user_spotify_refresh, get_redis, get_current_user_jwt
from ..utils.jwt import create_access_token
from ..utils.auth import store_refreshed_tokens
from ..services.spotify import SpotifyService
from requests.exceptions import HTTPError
from pydantic import BaseModel
from typing import List
from datetime import timedelta


router = APIRouter()


class PlaylistItem(BaseModel):
    id: str
    name: str
    public: bool


class AllPlaylistsResponse(BaseModel):
    playlists: List[PlaylistItem]


@router.get('/all', response_model=AllPlaylistsResponse, tags=['Spotify'])
def get_all_playlists(
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    all_playlists = spotify_service.get_all_playlists()
    return AllPlaylistsResponse(playlists=all_playlists["items"])


class Artist(BaseModel):
    name: str


class Album(BaseModel):
    name: str


class TrackItem(BaseModel):
    album: Album
    artists: List[Artist]
    name: str


class PlaylistTrack(BaseModel):
    track: TrackItem


class PlaylistTracks(BaseModel):
    items: List[PlaylistTrack]
    total: int


class Playlist(BaseModel):
    name: str
    tracks: PlaylistTracks


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


class TokenValidityResponse(BaseModel):
    user_spotify_token: bool


@router.get('/user', response_model=TokenValidityResponse, tags=['Spotify'])
def check_token_validity(
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    try:
        spotify_service.get_user_profile()
        return TokenValidityResponse(user_spotify_token=True)
    except HTTPError as error:
        if error.response.status_code == 401:
            return TokenValidityResponse(user_spotify_token=False)
        else:
            raise HTTPException(
                status_code=500,
                detail='Unexpected error while checking token validity',
            )


@router.post('/refresh', tags=['Spotify'])
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
        'spotify_status': spotify_status,
        'new_jwt': new_jwt
    }
