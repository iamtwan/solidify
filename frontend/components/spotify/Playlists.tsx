'use client';

import Playlist from "./Playlist";
import PlaylistInterface from "./PlaylistInterface";
import { useState, useEffect } from "react";
import Papa from 'papaparse';

export default function Playlists({ playlists }: {
  playlists: PlaylistInterface[]
}) {
  console.log(playlists);
  const [checkedPlaylists, setCheckedPlaylists] = useState<{ [key: string]: boolean }>({});

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
        const response = await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/private/${id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('spotify_token')}`
            }
        });
        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

const downloadSelected = async () => {
  for (const [id, checked] of Object.entries(checkedPlaylists)) {
      if (!checked) continue;

      const playlist = playlists.find(playlist => playlist.id === id) || {} as PlaylistInterface;
      const data = await fetchItems(id);
      const tracks = data.items.map((item: any) => [
          item.track.name,
          item.track.album.name,
          item.track.artists.map((artist: any) => artist.name)
      ]);

      const csvInfo = [
          ['Name', playlist.name],
          ['Total', data.total],
          ['Track Name', 'Album Name', 'Artist Names'],
          ...tracks
      ];

      const csv = Papa.unparse(csvInfo);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${playlist.name}.csv`;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
  }
}

const uploadSelected = async () => {
  for (const [id, checked] of Object.entries(checkedPlaylists)) {
    if (!checked) continue;

    await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/${id}`); // used to cache playlist in redis

    try {
      const response = await fetch(`http://127.0.0.1:8000/v1/google/upload/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('google_token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to upload playlist with id: ' + id);
      }

      console.log('uploaded playlist with id: ', id);
    } catch (error) {
      console.log(error);
      // refreshGoogleToken();
    }
  }
}

const refreshGoogleToken = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/v1/google/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('google_token')}`
      }
    });
  
    if (!response.ok) {
      throw new Error('Failed to refresh google token');
    }
  
    const data = await response.json();
    localStorage.setItem('google_token', data['new jwt']);
    console.log(data);
  } catch (error) {
    // login google
    console.log(error);
  }
}

  return <div>
    <label>
      <input type='checkbox' checked={isAnyPlaylistChecked()} onChange={handleSelectAll} />
      Select all
    </label>
    <button onClick={downloadSelected}>Download selected</button>
    <button onClick={uploadSelected}>Uploaded selected</button>
    {playlists.map(playlist => {
    return <Playlist key={playlist.id} 
      playlist={playlist} 
      checked={checkedPlaylists[playlist.id] || false}
      handleCheckboxChange={handleCheckboxChange}
    />
  })}
  </div>
}