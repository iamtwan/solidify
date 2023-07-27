'use client';

import styles from './page.module.css'
import React, { ChangeEvent, FormEvent, useState } from 'react';
import { CSVLink } from 'react-csv';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [inputValue, setInputValue] = useState('4pUmha8MJtm7RQBEETaSaI');
  const [csvData, setCsvData] = useState<string[][]>([]);

  const router = useRouter();

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://127.0.0.1:8000/v1/playlists/${inputValue}`);

      if (!response.ok) {
        throw new Error("Failed to fetch playlist");
      }

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

      const csvInfo = [
        ['Name', data.name], 
        ['Total', data.tracks.total], 
        ['Track Name', 'Album Name', 'Artist Names'], 
        ...tracks
      ];

      setCsvData(csvInfo);
    } catch (error) {
      console.error('Error: ', error);
    }
  };

  const login = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/v1/auth/login');
      const data = await response.json();

      router.push(data.url);
    } catch (error) {
      console.log(error);
    }

  }

  return (
    <main className={styles.main}>
      <div>
        <form onSubmit={handleSubmit}>
          <input type='text' value={inputValue} onChange={handleInputChange} />
          <button type='submit'>Submit</button>
        </form>
        <CSVLink data={csvData}>Download</CSVLink>
        <button onClick={login}>Login</button>
      </div>
    </main>
  )
}
