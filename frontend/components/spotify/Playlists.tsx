'use client';

import Playlist from "./Playlist";
import PlaylistInterface from "./PlaylistInterface";
import { useState, useEffect } from "react";
import Papa from 'papaparse';
import { login } from "@/services/api";

export default function Playlists({ playlists, googleToken }: {
  playlists: PlaylistInterface[],
  googleToken: string
}) {
  interface PlaylistInfo {
    checked: boolean,
    isUploading: boolean
  }

  const [checkedPlaylists, setCheckedPlaylists] = useState<{ [key: string]: PlaylistInfo }>({});
  const [playlistsToUpload, setPlaylistsToUpload] = useState<string[]>([]);

  useEffect(() => {
    let tempPlaylists: { [key: string ]: PlaylistInfo } = {};

    for(let playlist of playlists) {
      let tempPlaylist: PlaylistInfo = { checked: false, isUploading: false };
      tempPlaylists[playlist.id] = tempPlaylist;
    }

    setCheckedPlaylists(tempPlaylists);
  }, [playlists]);

  useEffect(() => {    
    const uploadPlaylists = async () => {
      for (let id of playlistsToUpload) {
        try {
          await uploadPlaylist(id);
        } catch (error) {
          console.log(error);
        }
      }
 
      setPlaylistsToUpload([]);
    }

    uploadPlaylists();
  }, [googleToken]);

  const handleCheckboxChange = (playlist: PlaylistInterface) => {
    setCheckedPlaylists(prevCheckedPlaylists => ({
      ...prevCheckedPlaylists,
      [playlist.id]: { ...prevCheckedPlaylists[playlist.id], checked: !prevCheckedPlaylists[playlist.id].checked }
    }));
  };

  const handleSelectAll = () => {
    const isAnyChecked = isAnyPlaylistChecked();
    const updatedPlaylists: { [key: string]: PlaylistInfo } = {};
    
    for (const key in checkedPlaylists) {
      updatedPlaylists[key] = { ...checkedPlaylists[key], checked: !isAnyChecked }
    }

    setCheckedPlaylists(updatedPlaylists);
  };

  const isAnyPlaylistChecked = () => Object.values(checkedPlaylists).some((playlist) => playlist.checked);

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
  for (const [id, playlistInfo] of Object.entries(checkedPlaylists)) {
    try {
      if (!playlistInfo.checked) continue;

      const data = await fetchItems(id);
      const tracks = data.tracks.items.map((item: any) => [
          item.track.name,
          item.track.album.name,
          item.track.artists.map((artist: any) => artist.name)
      ]);

      const csvInfo = [
          ['Name', data.name],
          ['Total', data.tracks.total],
          ['Track Name', 'Album Name', 'Artist Names'],
          ...tracks
      ];

      const csv = Papa.unparse(csvInfo);
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${data.name}.csv`;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); 
    } catch (error) {
      console.log(error);
    }
  }
}

  const uploadPlaylist = async (id: string) => {
      await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/${id}`); // used to cache playlist in redis

      const response = await fetch(`http://127.0.0.1:8000/v1/google/upload/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${googleToken}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to upload playlist with id: ' + id);
      }

      console.log('uploaded playlist with id: ' + id);
  }

  const uploadSelected = async () => {
    const playlists = [];

    for (const [id, playlistInfo] of Object.entries(checkedPlaylists)) {
      if (!playlistInfo.checked) continue;

      playlists.push(id);

      try {
        await uploadPlaylist(id);
      } catch (error) {
        console.log(error);

        try {
          setPlaylistsToUpload(playlists);
          await login('http://127.0.0.1:8000/v1/auth/google/login');
        } catch(error) {
          console.log(error);
        }

        break;
      }
    }
  }

// const refreshGoogleToken = async () => {
//   const googleToken = localStorage.getItem('google_token');

//   if (!googleToken) {
//     return false;
//   }

//   try {
//     const response = await fetch('http://127.0.0.1:8000/v1/google/refresh', {
//       method: 'POST',
//       headers: {
//         'Authorization': `Bearer ${googleToken}`
//       }
//     });
  
//     if (!response.ok) {
//       throw new Error('Failed to refresh google token');
//     }
  
//     const data = await response.json();
//     localStorage.setItem('google_token', data['new jwt']);
//     return true;
//   } catch (error) {
//     return false;
//   }
// }

  return <div>
    <label>
      <input type='checkbox' checked={isAnyPlaylistChecked()} onChange={handleSelectAll} />
      Select all
    </label>
    <button onClick={downloadSelected}>Download selected</button>
    <button onClick={uploadSelected}>Uploaded selected</button>
    {playlists.map(playlist => {
      const checked = checkedPlaylists[playlist.id] && checkedPlaylists[playlist.id].checked;

      return <Playlist key={playlist.id} 
        playlist={playlist} 
        checked={checked}
        handleCheckboxChange={handleCheckboxChange}
      />
  })}
  </div>
}