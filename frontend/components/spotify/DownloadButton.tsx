import { MouseEventHandler } from 'react';
import styles from '../spotify/Playlists/playlists.module.css';
import { Tooltip } from 'react-tooltip';

export default function DownloadButton({ onClick }: {
  onClick: MouseEventHandler
}) {
  return <>
  <span 
    className={styles.download} 
    onClick={onClick} 
    data-tooltip-id='download' 
    data-tooltip-content='Download'>
      download
  </span>
  <Tooltip id="download" />
</>;
}