import styles from './howitworks.module.css';
import Steps from './Steps';

export default function HowItWorks() {
  return <div className={styles['howitworks-container']}>
    <h1>How It Works</h1>

    <div className={styles.row}>
      <Steps title='Step 1' text='Enter the URL of the Spotify playlist you want to download.'/>
      <Steps title='Step 2' text='Click the download button to save the playlist as a CSV file.'/>
    </div>

    <div className={styles.row}>
      <Steps title='Step 3' text='Optionally, connect your Spotify account to access and download your own playlists.'/>
      <Steps title='Step 4' text='Optionally, upload directly to your google drive account.'/>
    </div>
  </div>
}