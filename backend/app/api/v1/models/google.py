from pydantic import BaseModel


class UploadPlaylist(BaseModel):
    status: str
