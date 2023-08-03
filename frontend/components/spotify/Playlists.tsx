import Playlist from "./Playlist"

export default function Playlists({ playlists }: {
  playlists: Playlist[]
}) {
  return <div>{playlists.map(playlist => {
    return <p>{playlist.name}</p>
  })}
  </div>
}