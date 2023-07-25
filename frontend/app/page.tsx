'use client';

import styles from './page.module.css'
import React, { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import Playlists from '@/components/spotify/Playlists';
import { fetchPlaylists, mutatePlaylists, downloadPlaylist, login } from '@/services/api';

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
      setPrevSpotifyKey(currSpotifyKey);
      trigger(currSpotifyKey);
    }

    if (currGoogleKey !== prevGoogleKey) {
      setPrevGoogleKey(currGoogleKey);
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
      const response = await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/${inputValue}`);

      if (!response.ok) {
        throw new Error("Failed to fetch playlist");
      }

      await downloadPlaylist(inputValue, false);
    } catch (error) {
      console.error('Error: ', error);
    }
  };

  const spotifyLogin = () => login('http://127.0.0.1:8000/v1/auth/spotify/login');

  return (
    <main className={styles.main}>
      <div>
        <h1>Enter a link to a Spotify playlist</h1>
        <form className={styles['playlist-form']} name='playlistForm' onSubmit={handleSubmit}>
          <input className={styles['input-field']} type='text' value={inputValue} onChange={handleInputChange} />
          <button type='submit' className={styles['download-button']}>Download</button>
        </form>
        <h1>Sign in to Spotify to view playlists</h1>
        {error ? 
        <button className={styles['login-button']} onClick={spotifyLogin}>Spotify Login</button> 
        : 
        <Playlists playlists={data?.playlists} googleToken={prevGoogleKey}/>}
      </div>
    </main>
  )
}
