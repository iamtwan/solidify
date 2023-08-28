'use client';

import PlaylistInterface from '../PlaylistInterface';
import styles from './playlist.module.css';
import { downloadPlaylist} from '@/services/api';
import DownloadButton from '../DownloadButton';
import UploadButton from '../UploadButton';

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
      <DownloadButton onClick={() => download(playlist.id)} />
      <UploadButton onClick={() => upload(playlist.id)} isUploading={isUploading} />
    </div>
  </div>
}