'use client';

import PlaylistInterface from './PlaylistInterface';

export default function Playlist({ playlist, checked, handleCheckboxChange }: {
    playlist: PlaylistInterface,
    checked: boolean,
    handleCheckboxChange: Function
}) {

    return <label>
        <input type='checkbox' checked={checked} onChange={() => handleCheckboxChange(playlist)}/>
        {playlist.name}
    </label>
}