import useSWRImmutable from 'swr/immutable';
import useSWRMutation from 'swr/mutation';

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
    const accessToken = localStorage.getItem('spotify_token') || '';

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

