import { MouseEventHandler } from 'react';
import styles from '../spotify/Playlists/playlists.module.css';
import { Tooltip } from 'react-tooltip';
import ReactLoading from 'react-loading';

export default function UploadButton({ onClick, isUploading }: {
  onClick: MouseEventHandler,
  isUploading?: boolean
}) {
  return <>
  <span 
    className={styles.upload} 
    onClick={onClick} 
    data-tooltip-id='upload' 
    data-tooltip-content='Upload'>
      {isUploading ? <ReactLoading type='spin' color='grey' width={24} height={24} /> : 'upload'}
  </span>
  <Tooltip id="upload" />
</>;
}