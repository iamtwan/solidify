'use client';

import PlaylistInterface from './PlaylistInterface';

export default function Playlist({ playlist, checked, isUploading, handleCheckboxChange }: {
    playlist: PlaylistInterface,
    checked: boolean,
    isUploading: boolean,
    handleCheckboxChange: Function
}) {    
    return <label>
        <input type='checkbox' checked={checked} onChange={() => handleCheckboxChange(playlist)}/>
        {playlist.name}
        {isUploading ? 'Uploading' : 'Upload'}
    </label>
   
}