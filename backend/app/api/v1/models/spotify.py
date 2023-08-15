from pydantic import BaseModel
from typing import List, Optional


class PlaylistItem(BaseModel):
    id: str
    name: str
    public: bool


class AllPlaylistsResponse(BaseModel):
    next: Optional[str]
    playlists: List[PlaylistItem]


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


class TokenValidity(BaseModel):
    user_spotify_token: bool
