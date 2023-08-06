import requests
import base64
import csv
import io

from typing import Optional, Any
from ..dependencies import get_redis


class SpotifyService:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            access_token: Optional[str] = None,
            refresh_token: Optional[str] = None
    ) -> None:
        self.base_url = 'https://api.spotify.com/v1'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = access_token
        self.refresh_token = refresh_token
        if not access_token:
            self.authenticate()

    @property
    def headers(self) -> dict:
        return {'Authorization': f'Bearer {self.token}'}

    def _request_token(self, data: dict, headers: dict) -> None:
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data['access_token']

    def authenticate(self) -> None:
        auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_string}'}
        data = {'grant_type': 'client_credentials'}
        self._request_token(data, headers)

    def refresh_access_token(self) -> Any:
        if not self.refresh_token:
            return

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_string}'}

        self._request_token(data, headers)

        return self.token

    def get_all_playlists(self) -> dict:
        fields = 'items(id,name,public)'
        url = f'{self.base_url}/me/playlists?fields={fields}'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def playlist_to_csv(self, playlist: dict) -> str:
        output = io.StringIO()
        fieldnames = ["track_name", "artist_name", "album_name"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for item in playlist['items']:
            track = item['track']
            writer.writerow({
                "track_name": track['name'],
                "artist_name": ', '.join(artist['name'] for artist in track['artists']),
                "album_name": track['album']['name'],
            })

        return output.getvalue()

    def cache_playlist(self, playlist_id: str, playlist: dict) -> None:
        csv_string = self.playlist_to_csv(playlist)
        redis = get_redis()
        redis.set(f'{playlist_id}_csv', csv_string, ex=3600)

    def get_protected_playlist(self, playlist_id: str) -> Any:
        fields = 'total,items(track(name,artists(name),album(name)))'
        url = f'{self.base_url}/playlists/{playlist_id}/tracks?fields={fields}'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        playlist = response.json()
        self.cache_playlist(playlist_id, playlist)

        return playlist

    def get_playlist(self, playlist_id: str) -> Any:
        fields = 'name,tracks.total,tracks.items(track(name,artists(name),album(name)))'
        url = f'{self.base_url}/playlists/{playlist_id}?fields={fields}'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        playlist = response.json()
        # self.cache_playlist(playlist_id, playlist)

        return playlist

    def get_user_profile(self) -> Any:
        url = f'{self.base_url}/me'

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()
