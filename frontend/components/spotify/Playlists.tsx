'use client';

import Playlist from "./Playlist";
import PlaylistInterface from "./PlaylistInterface";
import { useState, useEffect } from "react";
import Papa from 'papaparse';

export default function Playlists({ playlists }: {
  playlists: PlaylistInterface[]
}) {
  const [checkedPlaylists, setCheckedPlaylists] = useState<{ [key: string]: boolean }>({});
  const [csvData, setCsvData] = useState<string[][]>([]); 

  useEffect(() => {
    let tempPlaylists: { [key: string]: boolean } = {};

    for(let playlist of playlists) {
      tempPlaylists[playlist.id] = false;
    }

    setCheckedPlaylists(tempPlaylists);
  }, [playlists]);

  const handleCheckboxChange = (playlist: PlaylistInterface) => {
    setCheckedPlaylists(prevCheckedPlaylists => ({
      ...prevCheckedPlaylists,
      [playlist.id]: !prevCheckedPlaylists[playlist.id]
    }));
  };

  const handleSelectAll = () => {
    const isAnyChecked = isAnyPlaylistChecked();

    const updatedPlaylists = Object.keys(checkedPlaylists).reduce((acc, playlistId) => {
      acc[playlistId] = !isAnyChecked;
      return acc;
    }, {} as { [key: string]: boolean });

    setCheckedPlaylists(updatedPlaylists);
  };

  const isAnyPlaylistChecked = () => Object.values(checkedPlaylists).some((isChecked) => isChecked);

  const fetchItems = async (id: string) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/v1/spotify/private/${id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('spotify_token')}`
            }
        });
        const data = await response.json();
        return data.items;
    } catch (error) {
        console.error(error);
    }

    return [];
}

const downloadSelected = async () => {
  for (const [id, checked] of Object.entries(checkedPlaylists)) {
    if (checked) {
      const csvData = await fetchItems(id);
      console.log(csvData);
      const csv = Papa.unparse(csvData);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `playlist_${id}.csv`;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
}

  return <div>
    <label>
      <input type='checkbox' checked={isAnyPlaylistChecked()} onChange={handleSelectAll} />
      Select all
    </label>
    <button onClick={downloadSelected}>Download selected</button>
    {playlists.map(playlist => {
    return <Playlist key={playlist.id} 
      playlist={playlist} 
      checked={checkedPlaylists[playlist.id] || false}
      handleCheckboxChange={handleCheckboxChange}
    />
  })}
  </div>
}