from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.routes import spotify, spotify_auth, google_auth, google
from .api.v1.utils.auth import check_env_var
from dotenv import load_dotenv
from .api.v1.dependencies import get_spotify_service, get_redis


app = FastAPI()

load_dotenv()


@app.on_event("startup")
async def startup_event():
    required_env_vars = [
        'SECRET_KEY',
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET',
        'SPOTIFY_REDIRECT_URI',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'GOOGLE_REDIRECT_URI',
        'REDIS_PORT',
        'REDIS_HOST',
        'FRONT_ORIGIN'
    ]

    for var in required_env_vars:
        check_env_var(var)

    redis = get_redis()
    try:
        if redis.ping():
            print('Redis successfully connected')
    except ConnectionError:
        print('Unable to connect to Redis at startup')


# update for production
front_origin = check_env_var('FRONT_ORIGIN')
origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    front_origin
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
    prefix='/v1/spotify',
    dependencies=[Depends(get_spotify_service)]
)
