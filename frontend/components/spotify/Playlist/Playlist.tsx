'use client';

import PlaylistInterface from '../PlaylistInterface';
import styles from './playlist.module.css';
import playlistsStyles from '../Playlists/playlists.module.css';
import ReactLoading from 'react-loading';
import { downloadPlaylist} from '@/services/api';
import { Tooltip } from 'react-tooltip'

export default function Playlist({ playlist, checked, isUploading, handleCheckboxChange, upload }: {
    playlist: PlaylistInterface,
    checked: boolean,
    isUploading: boolean,
    handleCheckboxChange: Function,
    upload: Function
}) {
  const download = async (id: string) => {
    try {
      await downloadPlaylist(id, true);
    } catch (error) {
      console.log(error);
    }
  }

  return <div className={styles['playlist-container']}>
    <label className={styles['playlist-label']}>
      <input type='checkbox' checked={checked} onChange={() => handleCheckboxChange(playlist)}/>
      <span className={styles['playlist-name']}>{playlist.name}</span>
    </label>

    <div className={styles['upload-download']}>
      <span 
        className={playlistsStyles.download} 
        onClick={() => download(playlist.id)} 
        data-tooltip-id='download' 
        data-tooltip-content='Download'>
          download
      </span>
      <Tooltip id="download" />
      <span 
        className={playlistsStyles.upload} 
        onClick={() => upload(playlist.id)}
        data-tooltip-id='upload' 
        data-tooltip-content='Upload'>
          {isUploading ? <ReactLoading type='spin' color='grey' width={24} height={24} /> : 'upload'}
        </span>
        <Tooltip id="upload" />
    </div>
  </div>
}