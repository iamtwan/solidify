'use client';

import Playlist from "../Playlist/Playlist";
import PlaylistInterface from "../PlaylistInterface";
import { useState, useEffect } from "react";
import { fetchPlaylists, downloadPlaylist, uploadPlaylist, login } from "@/services/api";
import styles from './playlists.module.css';
import playlistStyles from '../Playlist/playlist.module.css';
import ReactLoading from 'react-loading';
import DownloadButton from "../DownloadButton";
import UploadButton from "../UploadButton";
import { BACKEND_URL } from '@/services/apiConfig';

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

  const upload = async (id: string) => {
    try {
      setPlaylistsToUpload([...playlistsToUpload, id]);
      setPlaylistIsUploading(id, true);
      await uploadPlaylist(id);
      setPlaylistIsUploading(id, false);
    } catch (error) {
      console.log(error);

      try {
        await login(`${BACKEND_URL}/v1/auth/google/login`);
      } catch(error) {
        console.log(error);
      } 
    } finally {
      setPlaylistIsUploading(id, false);
    }
  }

  const uploadSelected = async () => {
    for (const [id, playlistInfo] of Object.entries(checkedPlaylists)) {
      if (!playlistInfo.checked) continue;
      await upload(id);
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

  const spotifyLogin = () => login(`${BACKEND_URL}/v1/auth/spotify/login`);

  return <div className={styles['playlists-container']}>
    <div className={styles['playlists-inner-container']}>
      <div className={styles['playlists-options']}>
        <input type='checkbox' checked={isAnyPlaylistChecked()} onChange={handleSelectAll} />
      
        <div className={playlistStyles['upload-download']}>
          <DownloadButton onClick={downloadSelected} />
          <UploadButton onClick={uploadSelected} />
        </div>
      </div>

      {error ? <button className={styles['login-button']} onClick={spotifyLogin}>Spotify login</button> : !data ? 
      <div className={styles['playlists-loading']}><ReactLoading type='spin' color='grey' width={30} height={30}/></div> : 
      <div className={styles['playlists-list']}>
        {data.playlists.map((playlist: PlaylistInterface) => {
          const checked = (checkedPlaylists[playlist.id] && checkedPlaylists[playlist.id].checked) || false;
          const isUploading = (checkedPlaylists[playlist.id] && checkedPlaylists[playlist.id].isUploading) || false;

          return <Playlist key={playlist.id} 
            playlist={playlist} 
            checked={checked}
            isUploading={isUploading}
            handleCheckboxChange={handleCheckboxChange}
            upload={upload}
          /> 
        })}

        <div className={styles['pagination-container']}>
          <button 
            disabled={pageIndex <= 0} 
            onClick={() => setPageIndex(pageIndex - 1)}
            className={styles['pagination-button']}>
              Prev
          </button>
          <button 
            disabled={!data.next} 
            onClick={() => setPageIndex(pageIndex + 1)}
            className={styles['pagination-button']}>
              {isLoading ? <ReactLoading type='spin' color='grey' width={10} height={13}/> : 'Next'}
          </button>
        </div>
      </div>
      }
    </div>
  </div>
}