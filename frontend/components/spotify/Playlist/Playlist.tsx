'use client';

import PlaylistInterface from '../PlaylistInterface';
import styles from './playlist.module.css';
import playlistsStyles from '../Playlists/playlists.module.css';

export default function Playlist({ playlist, checked, isUploading, handleCheckboxChange }: {
    playlist: PlaylistInterface,
    checked: boolean,
    isUploading: boolean,
    handleCheckboxChange: Function
}) {
  return <div className={styles['playlist-container']}>
    <label className={styles['playlist-label']}>
      <input type='checkbox' checked={checked} onChange={() => handleCheckboxChange(playlist)}/>
      <span className={styles['playlist-name']}>{playlist.name}</span>
    </label>

    <div className={styles['upload-download']}>
      <span className={playlistsStyles.download}>download</span>
      <span className={playlistsStyles.upload}>upload</span>
    </div>
  </div>
}