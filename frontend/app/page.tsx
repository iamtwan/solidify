'use client';

import styles from './page.module.css'
import React, { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import { CSVLink } from 'react-csv';
import Playlists from '@/components/spotify/Playlists';
import { fetchPlaylists, mutatePlaylists } from '@/services/api';

export default function Page() {
  const [inputValue, setInputValue] = useState('4pUmha8MJtm7RQBEETaSaI');
  const [csvData, setCsvData] = useState<string[][]>([]);
  const [mounted, setMounted] = useState(false);

  const [prevSpotifyKey, setPrevSpotifyKey] = useState('');
  const [prevGoogleKey, setPrevGoogleKey] = useState('');

  const { data, error, isLoading } = fetchPlaylists(mounted);
  const { trigger } = mutatePlaylists();

  const handleStorageChange = () => {
    const currSpotifyKey = localStorage.getItem('spotify_token') || '';
    const currGoogleKey = localStorage.getItem('google_token') || '';

    if (currSpotifyKey !== prevSpotifyKey) {
      trigger(currSpotifyKey);
    }

    if (currGoogleKey !== prevGoogleKey) {

    }
  }

  useEffect(() => {
    setMounted(true);
    setPrevSpotifyKey(localStorage.getItem('spotify_token') || '');
    setPrevGoogleKey(localStorage.getItem('google_token') || '');

    window.addEventListener('storage', handleStorageChange);
  }, [])

  if (isLoading) {
    return <div>Loading playlists</div>;
  }
  
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

  const login = async (url: string) => {
    try {
      const response = await fetch(url);
      const data = await response.json();

      const windowFeatures ='toolbar=no, menubar=no, width=600, height=700, top=100, left=100';
      window.open(data.url, '_blank', windowFeatures);
    } catch (error) {
      console.log(error);
    }
  }

  const spotifyLogin = () => login('http://127.0.0.1:8000/v1/auth/spotify/login');

  const googleLogin = () => login('http://127.0.0.1:8000/v1/auth/google/login');

  return (
    <main className={styles.main}>
      <div>
        <form onSubmit={handleSubmit}>
          <input type='text' value={inputValue} onChange={handleInputChange} />
          <button type='submit'>Submit</button>
        </form>
        <CSVLink data={csvData}>Download</CSVLink>
        {error ? (<button onClick={spotifyLogin}>Spotify Login</button>) : (<Playlists playlists={data?.playlists} />)}
      </div>
    </main>
  )
}
