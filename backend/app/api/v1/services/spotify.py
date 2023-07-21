import requests
import base64
import time


class SpotifyService:
    def __init__(self, client_id, client_secret):
        self.base_url = 'https://api.spotify.com/v1'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires = 0
        self.authenticate()

    # Client Credentials OAuth2 Flow
    def authenticate(self):
        auth_string = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {'Authorization': f'Basic {auth_string}'}
        data = {'grant_type': 'client_credentials'}

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expires = time.time() + token_data['expires_in']

    def check_access_token(self):
        # expiry epoch time
        print(self.token_expires)
        if time.time() > self.token_expires:
            self.authenticate()

    def get_playlist(self, playlist_id):
        print('test')
        self.check_access_token()

        fields = 'name,tracks.total,tracks.items(track(name,artists(name),album(name)))'
        url = f'{self.base_url}/playlists/{playlist_id}?fields={fields}'
        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
