from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.routes import playlists, spotify_auth, google_auth
from dotenv import load_dotenv
from .api.v1.dependencies import get_spotify_service


load_dotenv()

app = FastAPI()

# update for production
origins = [
    'http://localhost:3000'
]

# update for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['*']
)

app.include_router(spotify_auth.router, prefix='/v1/auth')
app.include_router(google_auth.router, prefix='/v1/auth')
app.include_router(
    playlists.router,
    prefix='/v1/playlists',
    dependencies=[Depends(get_spotify_service)]
)
