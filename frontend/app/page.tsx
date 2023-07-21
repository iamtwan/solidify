'use client';

import styles from './page.module.css';
import React, { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import Playlists from '@/components/spotify/Playlists/Playlists';
import { mutatePlaylists, downloadPlaylist, login } from '@/services/api';

export default function Page() {
  const [inputValue, setInputValue] = useState('4pUmha8MJtm7RQBEETaSaI');

  const [prevSpotifyKey, setPrevSpotifyKey] = useState('');
  const [prevGoogleKey, setPrevGoogleKey] = useState('');

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
    setPrevSpotifyKey(localStorage.getItem('spotify_token') || '');
    setPrevGoogleKey(localStorage.getItem('google_token') || '');

    window.addEventListener('storage', handleStorageChange);
  }, [])

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

  return (
    <main className={styles.main}>
      <div>
        <h2>Enter a link to a Spotify playlist</h2>
        <form className={styles['playlist-form']} name='playlistForm' onSubmit={handleSubmit}>
          <input className={styles['input-field']} type='text' value={inputValue} onChange={handleInputChange} />
          <button type='submit' className={styles['download-button']}>Download</button>
        </form>
        <Playlists googleToken={prevGoogleKey}/>
      </div>
    </main>
  )
}
