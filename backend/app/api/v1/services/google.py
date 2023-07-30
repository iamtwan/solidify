import requests


class GoogleService:
    def __init__(
            self,
            access_token=None,
            refresh_token=None
    ):
        self.base_url = 'https://www.googleapis.com/upload/drive/v3'
        self.token_url = 'https://oauth2.googleapis.com/token'
        self.token = access_token
        self.refresh_token = refresh_token

    # def check_access_token(self):
    #     if not self.token or time.time() > self.token_expires:
    #         self.refresh_access_token()

    def upload_file(self, playlist_id, csv_string):
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
