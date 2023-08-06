from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_spotify_service, get_user_spotify_service
from ..services.spotify import SpotifyService
from requests.exceptions import HTTPError
from pydantic import BaseModel
from typing import List


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


class Track(BaseModel):
    name: str
    artists: List[Artist]
    album: Album


class Playlist(BaseModel):
    name: str
    total: int
    items: List[Track]


@router.get('/private/{playlist_id}', response_model=Playlist, tags=['Spotify'])
def get_protected_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_user_spotify_service)
):
    playlist = spotify_service.get_protected_playlist(playlist_id)
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


@router.get('/{playlist_id}', response_model=Playlist, tags=['Spotify'])
def get_playlist(
    playlist_id: str,
    spotify_service: SpotifyService = Depends(get_spotify_service)
):
    playlist = spotify_service.get_playlist(playlist_id)
    return playlist
