from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.routes import spotify, spotify_auth, google_auth, google
from dotenv import load_dotenv
from .api.v1.dependencies import get_spotify_service


load_dotenv()

app = FastAPI()

# update for production
origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

# update for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(spotify_auth.router, prefix='/v1/auth')
app.include_router(google_auth.router, prefix='/v1/auth')
app.include_router(google.router, prefix='/v1/google')
app.include_router(
    spotify.router,
    prefix='/v1/playlists',
    dependencies=[Depends(get_spotify_service)]
)
