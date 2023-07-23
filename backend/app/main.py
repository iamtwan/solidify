from fastapi import FastAPI, Depends
from .api.v1.routes import playlists, spotify_auth
from dotenv import load_dotenv
from .api.v1.dependencies import get_spotify_service


load_dotenv()

app = FastAPI()

app.include_router(spotify_auth.router, prefix='/v1/auth')
app.include_router(playlists.router, prefix='/v1/playlists', dependencies=[Depends(get_spotify_service)])
