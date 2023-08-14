'use client';

import Playlist from "../Playlist/Playlist";
import PlaylistInterface from "../PlaylistInterface";
import { useState, useEffect } from "react";
import { fetchPlaylists, downloadPlaylist, uploadPlaylist, login } from "@/services/api";
import styles from './playlists.module.css';
import playlistStyles from '../Playlist/playlist.module.css';

export default function Playlists({ googleToken }: {
  googleToken: string
}) {
  interface PlaylistInfo {
    checked: boolean,
    isUploading: boolean
  }

  const [checkedPlaylists, setCheckedPlaylists] = useState<{ [key: string]: PlaylistInfo }>({});
  const [playlistsToUpload, setPlaylistsToUpload] = useState<string[]>([]);
  const [mounted, setMounted] = useState(false);
  const [pageIndex, setPageIndex] = useState(0);

  const { data, error, isLoading } = fetchPlaylists(mounted, pageIndex);

  useEffect(() => {
    if (data) {
      let tempPlaylists: { [key: string ]: PlaylistInfo } = {};

      for(let playlist of data.playlists) {
        let tempPlaylist: PlaylistInfo = { checked: false, isUploading: false };
        tempPlaylists[playlist.id] = tempPlaylist;
      }

      setCheckedPlaylists(tempPlaylists);
  }
  }, [data]);

  useEffect(() => {    
    const uploadPlaylists = async () => {
      for (let id of playlistsToUpload) {
        try {
          setPlaylistIsUploading(id, true);
          await uploadPlaylist(id);
        } catch (error) {
          console.log(error);
        } finally {
          setPlaylistIsUploading(id, false);
        }
      }
 
      setPlaylistsToUpload([]);
    }

    uploadPlaylists();
  }, [googleToken]);

  useEffect(() => {
    setMounted(true);
  }, [])

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

  const downloadSelected = async () => {
    for (const [id, playlistInfo] of Object.entries(checkedPlaylists)) {
      try {
        if (!playlistInfo.checked) continue;
        await downloadPlaylist(id, true);
      } catch (error) {
        console.log(error);
      }
    }
  }

  const uploadSelected = async () => {
    const playlists = [];

    for (const [id, playlistInfo] of Object.entries(checkedPlaylists)) {
      if (!playlistInfo.checked) continue;

      playlists.push(id);

      try {
        setPlaylistIsUploading(id, true);
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
      } finally {
        setPlaylistIsUploading(id, false);
      }
    }
  }

  const setPlaylistIsUploading = (id: string, isUploading: boolean) => {
    setCheckedPlaylists(prevCheckedPlaylists => ({
      ...prevCheckedPlaylists,
      [id]: { ...prevCheckedPlaylists[id], isUploading }
    }));
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

  const spotifyLogin = () => login('http://127.0.0.1:8000/v1/auth/spotify/login');

  return <div className={styles['playlists-container']}>
    <div className={styles['playlists-inner-container']}>
      <div className={styles['playlists-options']}>
        <input type='checkbox' checked={isAnyPlaylistChecked()} onChange={handleSelectAll} />
      
        <div className={playlistStyles['upload-download']}>
          <span onClick={downloadSelected} className={styles.download}>download</span>
          <span onClick={uploadSelected} className={styles.upload}>upload</span>
        </div>
      </div>

      {error ? <button className={styles['login-button']} onClick={spotifyLogin}>Spotify login</button> : isLoading ? 
      <div className={styles['login-button']}>Loading...</div> : 
      <div>
        {data.playlists.map((playlist: PlaylistInterface) => {
          const checked = (checkedPlaylists[playlist.id] && checkedPlaylists[playlist.id].checked) || false;
          const isUploading = (checkedPlaylists[playlist.id] && checkedPlaylists[playlist.id].isUploading) || false;

          return <Playlist key={playlist.id} 
            playlist={playlist} 
            checked={checked}
            isUploading={isUploading}
            handleCheckboxChange={handleCheckboxChange}
          /> 
      })}

      <button disabled={pageIndex <= 0} onClick={() => setPageIndex(pageIndex - 1)}>Prev</button>
      <button disabled={!data.next} onClick={() => setPageIndex(pageIndex + 1)}>Next</button>
      </div>
      }
    </div>
  </div>
}