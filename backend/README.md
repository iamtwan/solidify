# Solidify Backend

Solidify Backend is the server-side component of the Solidify Spotify playlist exporter tool. This component handles API requests, user OAuth authentication (integration with external services like Spotify and Google Drive), and playlist processing.

## Features

- **API Endpoints**: Expose endpoints to fetch public and private Spotify playlists.
- **Spotify Integration**: OAuth2 authentication for protected Spotify playlist retrieval.
- **Google Drive Integration**: Optional OAuth2 authentication to allow users to upload playlists directly to Google Drive.
- **Redis Cache**: Efficient handling of dependency requests using Redis for caching.
- **Environment Configuration**: Easy setup with environment variables.

## Getting Started

These instructions will guide you through setting up the backend component on your local machine for development and testing purposes.

### Prerequisites

- **Python**: Version 3.7 or newer is required.
- **Redis**: A running Redis instance is needed.
- **Developer Credentials**: You'll need (mandatory) developer credentials for [Spotify](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) and (optionally) for [Google](https://cloud.google.com/apis/docs/getting-started#creating_a_google_project), for OAuth upload functionality.

### Environment Configuration

Create a `.env` file in the backend `app` root directory with the following variables (ensure you insert your own credentials):

- SECRET_KEY=`run openssl rand -hex 32`
- SPOTIFY_CLIENT_ID=your_spotify_client_id
- SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
- SPOTIFY_REDIRECT_URI=localhost:3000/auth/spotify/callback
- GOOGLE_CLIENT_ID=your_google_client_id
- GOOGLE_CLIENT_SECRET=your_google_client_secret
- GOOGLE_REDIRECT_URI=localhost:3000/auth/google/callback
- REDIS_URL=your_redis_connection_url
- REDIS_HOST=redis (or 'localhost' for local development)

### Installation

1. Clone the repository or backend folder.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the FastAPI server locally with `uvicorn main:app --reload`.

### Usage

This backend is designed to work with the Solidify front-end. All interactions with the Solidify APIs should be handled through the front-end interface or through direct API calls using the provided documentation. You may access the live Solidify API documentation locally at `localhost:8000/docs#/Authorization`.

### Deployment

For production deployment, please refer to the provided recommended [Dockerfile](https://github.com/iamtwan/solidify/tree/main#installation) and corresponding deployment guide.

### Acknowledgments

The backend was designed with simplicity, performance, and user privacy (short-lived sessions) in mind. Many thanks to the FastAPI framework to accomplish this with Python.
