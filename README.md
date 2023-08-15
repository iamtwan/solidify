# Solidify

Solidify is a lightweight Spotify playlist tool designed to provide users with a way to retrieve and process their Spotify playlists into an exportable .csv format. Whether you're looking to archive your playlists for safekeeping or migrate to another service that accepts .csv format, Solidify is the right tool for you.

## Features

- Export Spotify playlists into .csv format.
- Option to download a .csv file, copy its contents to the clipboard, or upload it to Google Drive.
- Connect to your Spotify account to access both public and private playlists.
- Single-page user-friendly web application interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To set up the environment, you will need [Docker](https://www.docker.com/), which encapsulates all the required packages and libraries. Additionally, developer credentials for Spotify (mandatory) and Google (optional) are essential. These credentials are utilized as environment variables on the server-side, playing a crucial role in the app's core functionalities. Without them, the app will not function properly.

Please refer to the [back-end README](https://github.com/iamtwan/solidify/blob/main/backend/README.md#environment-configuration) for detailed instructions on configuring the `.env` file and integrating these credentials into the application.

### Installation

To install Solidify, follow these steps:

- Fork and clone the repository, or just clone it directly.
- Use Docker to build and run Solidify with the following command within the repo directory: `docker-compose up --build`.
- You can then access Solidify at `http://localhost:3000/` or via the deployed server host.

## Usage

- Provide a valid public Spotify playlist link (e.g. https://open.spotify.com/playlist/7Clo0AeCf2rq7Y2NcdGPou), and Solidify will respond with a .csv download link and a copy-to-clipboard link.
- Connect your Spotify account to access your private playlists. Once connected, Solidify will display a list of your playlists. Select one, and Solidify will provide a .csv download link and a copy-to-clipboard link.
- Optionally, sign into your Google account for an instant upload of the .csv file to your Google Drive.

## Deployment

The app is deployed at `https://www.solidify-exporter.com` for public use. However, users who wish to deploy the app themselves should follow the provided [Installation](https://github.com/iamtwan/solidify#installation) instructions for local development deployment.

## Built With

- Frontend: Next.js, TypeScript, and TailwindCSS.
- Backend: FastAPI, Python, and Redis.

## Contributing

Solidify is not open for contributions at this time. However, we encourage anyone to fork the repository for their own use.

## Authors

- Back-end - [@iamtwan](https://github.com/iamtwan)
- Front-end - [@Itttz](https://github.com/Itttz)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more details.

## Disclosure

The Solidify app does not provide access to any music files. Solidify only provides .csv with text-only playlist data, respecting the Spotify API's "stream-ripping" policy. Solidify does not store any user data beyond the client session and does not require access to any critical user credentials or resources.

## Acknowledgments

While the general concept of Solidify is not unique and similar tools exist or have been built in the past, Solidify does not take any direct inspiration and it primarily serves as a functional portfolio piece for the authors.
