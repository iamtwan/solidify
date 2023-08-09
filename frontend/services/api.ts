import useSWRImmutable from 'swr/immutable';

const fetcher = async (url: string, headers: Headers) => {
    console.log(url, headers.get('Authorization'));
    const response = await fetch(url, { headers });

    if (!response.ok) {
        throw new Error(await response.json());
    }

    return await response.json();
}

export const fetchPlaylists = (mounted: boolean) => {
    const headers: Headers = new Headers();

    if (mounted) { 
        console.log(localStorage);
        headers.set('Authorization', `Bearer ${localStorage.getItem('spotify_token')}`);
    }

    console.log(mounted);

    const { data, error, isLoading } = useSWRImmutable(mounted ? 'http://127.0.0.1:8000/v1/spotify/all' : null, url => fetcher(url, headers), {
        shouldRetryOnError: false
    });

    return {
        data,
        error,
        isLoading: mounted ? isLoading : true
    };
  }
