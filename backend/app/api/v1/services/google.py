import requests

from typing import Optional, Any


class GoogleService:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            access_token: Optional[str] = None,
            refresh_token: Optional[str] = None
    ):
        self.base_url = 'https://www.googleapis.com/upload/drive/v3'
        self.token_url = 'https://oauth2.googleapis.com/token'
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = access_token
        self.refresh_token = refresh_token

    @property
    def headers(self) -> dict:
        return {'Authorization': f'Bearer {self.token}'}

    def _request_token(self, data: dict) -> None:
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.token = token_data['access_token']

    def refresh_access_token(self) -> Any:
        if not self.refresh_token:
            return

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        self._request_token(data)

        return self.token

    def upload_file(self, playlist_id, csv_string) -> Any:
        url = f'{self.base_url}/files?uploadType=multipart'
        boundary = 'foo_bar_baz'
        body = (
            f'--{boundary}\n'
            f'Content-Type: application/json; charset=UTF-8\n\n'
            f'{{"name": "{playlist_id}"}}\n'
            f'--{boundary}\n'
            f'Content-Type: text/csv\n\n'
            f'{csv_string}\n'
            f'--{boundary}--'
        )
        content_length = len(body.encode('utf-8'))
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': f'multipart/related; boundary={boundary}',
            'Content-Length': str(content_length)
        }

        response = requests.post(
            url,
            headers=headers,
            data=body.encode('utf-8')
        )
        response.raise_for_status()

        return response.status_code, response.json()
