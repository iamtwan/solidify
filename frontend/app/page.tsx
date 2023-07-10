'use client';

import styles from './page.module.css'
import { ChangeEvent, FormEvent, useState } from 'react';
import { CSVLink } from 'react-csv';

export default function Home() {
  const [inputValue, setInputValue] = useState('https://api.spotify.com/v1/playlists/4pUmha8MJtm7RQBEETaSaI');
  const [csvData, setCsvData] = useState([]);

  const client_id = 'a75a997107f84884b379d97ac220c3f1';
  const client_secret = '4c6f998a4cd64603a77b4c783f732dcc';

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const tokenResponse = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
          'Authorization': 'Basic ' + (Buffer.from(client_id + ':' + client_secret).toString('base64')),
        },
        body: new URLSearchParams({
          'grant_type': 'client_credentials'
        })
      });
  
      const tokenData = await tokenResponse.json();
      const response = await fetch(inputValue, {
        headers: {
          'Authorization': 'Bearer ' + tokenData.access_token
        }
      });
  
      const data = await response.json();
      const tracks = [];
      
      for (const item of data.tracks.items) {
        const track = [item.track.name, item.track.album.name];
        const artists = [];

        for (let artist of item.track.artists) {
          artists.push(artist.name);
        }

        track.push(artists);
        tracks.push(track);
      }

      const csvData = [['Name', data.name], ['Total', data.tracks.total], ['Track Name', 'Album Name', 'Artist Names'], ...tracks];
      setCsvData(csvData);
    } catch (error) {
      console.error('Error: ', error);
    }
  };

  return (
    <main className={styles.main}>
      <div>
        <form onSubmit={handleSubmit}>
          <input type='text' value={inputValue} onChange={handleInputChange} />
          <button type='submit'>Submit</button>
        </form>
        <CSVLink data={csvData}>Download</CSVLink>
      </div>
    </main>
  )
}
