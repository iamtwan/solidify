'use client';

import styles from './page.module.css';
import React, { ChangeEvent, FormEvent, useState, useEffect } from 'react';
import HowItWorks from '@/components/howitworks/HowItWorks';
import Playlists from '@/components/spotify/Playlists/Playlists';
import { mutatePlaylists, downloadPlaylist } from '@/services/api';
import 'react-tooltip/dist/react-tooltip.css';

export default function Page() {
  const [inputValue, setInputValue] = useState('');

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
      const url = new URL(inputValue);
      const playlistId = url.pathname.split("/").pop();

      if (url.hostname !== 'open.spotify.com' || !playlistId) {
        throw new Error('Invalid domain name');
      }

      await downloadPlaylist(playlistId, false);
    } catch (error) {
      console.error('Error: ', error);
    }
  };

  return (
    <main className={styles.main}>
      <HowItWorks />
      <div className={styles['playlist-download']}>
        <h2 className={styles['download-title']}>Download Spotify Playlist as CSV</h2>
        <form className={styles['playlist-form']} name='playlistForm' onSubmit={handleSubmit}>
          <input className={styles['input-field']} type='text' value={inputValue} onChange={handleInputChange} placeholder='Enter Spotify Playlist Link'/>
          <button type='submit' className={styles['download-button']}>Download</button>
        </form>
      </div>
            
      <Playlists googleToken={prevGoogleKey}/>
    </main>
  )
}
