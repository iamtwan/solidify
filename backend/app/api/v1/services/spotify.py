import requests
import base64
import time
import csv
import io


class SpotifyService:
    def __init__(
            self,
            client_id,
            client_secret,
            access_token=None,
            refresh_token=None
    ):
        self.base_url = 'https://api.spotify.com/v1'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = access_token
        self.refresh_token = refresh_token
        self.token_expires = 0
        if not access_token:
            self.authenticate()

    def authenticate(self):
        auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_string}'}
        data = {'grant_type': 'client_credentials'}

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expires = time.time() + token_data['expires_in']

    def check_access_token(self):
        if not self.token or time.time() > self.token_expires:
            self.refresh_access_token()

    def refresh_access_token(self):
        if not self.refresh_token:
            return

        auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_string}'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expires = time.time() + token_data['expires_in']

    def get_all_playlists(self):
        self.check_access_token()

        fields = 'items(id,name,public)'
        url = f'{self.base_url}/me/playlists?fields={fields}'
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(url, headers=headers)
        print(response.content)
        response.raise_for_status()

        return response.json()

    def playlist_to_csv(self, playlist):
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

    def get_protected_playlist(self, playlist_id):
        self.check_access_token()

        fields = 'total,items(track(name,artists(name),album(name)))'
        url = f'{self.base_url}/playlists/{playlist_id}/tracks?fields={fields}'
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        playlist = response.json()
        csv_string = self.playlist_to_csv(playlist)
        from ..dependencies import get_redis
        redis = get_redis()
        redis.set(f'{playlist_id}_csv', csv_string, ex=3600)

        return playlist

    def get_playlist(self, playlist_id):
        self.check_access_token()

        fields = 'name,tracks.total,tracks.items(track(name,artists(name),album(name)))'
        url = f'{self.base_url}/playlists/{playlist_id}?fields={fields}'
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        playlist = response.json()
        csv_string = self.playlist_to_csv(playlist)
        from ..dependencies import get_redis
        redis = get_redis()
        redis.set(f'{playlist_id}_csv', csv_string, ex=3600)

        return playlist
