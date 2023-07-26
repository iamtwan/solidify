import useSWR from 'swr';

const fetcher = async (url: string, headers: HeadersInit = new Headers()) => {
    const response = await fetch(url, { headers });

    if (!response.ok) {
        throw new Error("Error: ", await response.json());
    }

    return await response.json();
}

export const fetchPlaylists = () => {
    const headers: HeadersInit = new Headers();
    headers.set('Authorization', `Bearer ${localStorage.getItem('spotify_token')}`);
    
    const { data, error, isLoading } = useSWR('http://127.0.0.1:8000/v1/spotify/all', url => fetcher(url, headers));

    return {
        data,
        error,
        isLoading
    };
  }
