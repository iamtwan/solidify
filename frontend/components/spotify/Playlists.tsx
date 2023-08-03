'use client';

import Playlist from "./Playlist";
import PlaylistInterface from "./PlaylistInterface";
import { useState, useEffect } from "react";

export default function Playlists({ playlists }: {
  playlists: PlaylistInterface[]
}) {
  const [checkedPlaylists, setCheckedPlaylists] = useState<{ [key: string]: boolean }>({});

  useEffect(() => {
    let tempPlaylists: { [key: string]: boolean } = {};

    for(let playlist of playlists) {
      tempPlaylists[playlist.id] = false;
    }

    setCheckedPlaylists(tempPlaylists);
  }, playlists);

  const handleCheckboxChange = (playlist: PlaylistInterface) => {
    setCheckedPlaylists(prevCheckedPlaylists => ({
      ...prevCheckedPlaylists,
      [playlist.id]: !prevCheckedPlaylists[playlist.id]
    }));
  };

  const handleSelectAll = () => {
    const updatedPlaylists = Object.keys(checkedPlaylists).reduce((acc, playlistId) => {
      acc[playlistId] = !isAnyPlaylistChecked();
      return acc;
    }, {} as { [key: string]: boolean });

    setCheckedPlaylists(updatedPlaylists);
  };

  const isAnyPlaylistChecked = () => Object.values(checkedPlaylists).some((isChecked) => isChecked);

  return <div>
    <label>
      <input type='checkbox' checked={isAnyPlaylistChecked()} onClick={handleSelectAll} />
      Select all
    </label>
    {playlists.map(playlist => {
    return <Playlist key={playlist.id} 
      playlist={playlist} 
      checked={checkedPlaylists[playlist.id]}
      handleCheckboxChange={handleCheckboxChange}
    />
  })}
  </div>
}