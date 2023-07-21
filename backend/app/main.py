from fastapi import FastAPI
from .api.v1.routes import playlists

app = FastAPI()

app.include_router(playlists.router, prefix='/v1/playlists')

@app.get('/')
def read_root():
    return {'Solidify': 'Server Connected'}
