import useSWRImmutable from 'swr/immutable';
import useSWRMutation from 'swr/mutation';
import Papa from 'papaparse';

const fetcher = async (url: string, { arg } : { arg: string }) => {
    const headers: Headers = new Headers();
    headers.set('Authorization', `Bearer ${arg}`);

    const response = await fetch(url, { headers });

    if (!response.ok) {
        throw new Error(await response.json());
    }

    return await response.json();
}

export const fetchPlaylists = (mounted: boolean) => {
    const accessToken = (mounted && localStorage.getItem('spotify_token')) || '';

    const { data, error, isLoading } = useSWRImmutable(mounted ? 'http://127.0.0.1:8000/v1/spotify/all' : null, 
    url => fetcher(url, { arg: accessToken} ));

    return {
        data,
        error,
        isLoading: mounted ? isLoading : true,
    };
}

export const mutatePlaylists = () => {
    const { trigger, isMutating } = useSWRMutation('http://127.0.0.1:8000/v1/spotify/all', fetcher);

    return { 
        trigger,
        isMutating
    }
}

export const downloadPlaylist = async (id: string, isPrivate: boolean) => {
    try {
        const data = await fetchItems(id, isPrivate);
        const tracks = data.tracks.items.map((item: any) => [
            item.track.name,
            item.track.album.name,
            item.track.artists.map((artist: any) => artist.name)
        ]);
    
        const csvInfo = [
            ['Name', data.name],
            ['Total', data.tracks.total],
            ['Track Name', 'Album Name', 'Artist Names'],
            ...tracks
        ];
    
        const csv = Papa.unparse(csvInfo);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${data.name}.csv`;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);  
    } catch (error) {
        console.log(error);
    }
}

export const uploadPlaylist = async (id: string) => {
    await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/${id}`); // used to cache playlist in redis

    const response = await fetch(`http://127.0.0.1:8000/v1/google/upload/${id}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('google-token')}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to upload playlist with id: ' + id);
    }

    console.log('uploaded playlist with id: ' + id);
}

const fetchItems = async (id: string, isPrivate: boolean) => {
    try {
        let response;

        if (isPrivate) {
            response = await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/private/${id}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('spotify_token')}`
                }
            });
        } else {
            response = await fetch(`http://127.0.0.1:8000/v1/spotify/playlists/${id}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

export const login = async (url: string) => {
    try {
      const response = await fetch(url);
      const data = await response.json();

      const windowFeatures ='toolbar=no, menubar=no, width=600, height=700, top=100, left=100';
      window.open(data.url, '_blank', windowFeatures);
    } catch (error) {
      console.log(error);
    }
}
