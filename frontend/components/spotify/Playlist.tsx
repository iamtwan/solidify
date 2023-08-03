import PlaylistInterface from './PlaylistInterface';

export default function Playlist({ playlist, checked, handleCheckboxChange }: {
    playlist: PlaylistInterface,
    checked: boolean,
    handleCheckboxChange: Function
}) {
    return <label>
        <input type='checkbox' checked={checked} onClick={() => handleCheckboxChange(playlist)}/>
        {playlist.name}
    </label>
}