
from pydantic import BaseModel


class RefreshTokens(BaseModel):
    service_status: str
    new_jwt: str


class LoginResponse(BaseModel):
    url: str


class CallbackResponse(BaseModel):
    jwt: str
    status: str
