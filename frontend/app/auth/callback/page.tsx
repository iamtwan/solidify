'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Callback() {
    const router = useRouter();

    const fetchToken = async (code: string, state: string) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/v1/auth/callback?code=${code}&state=${state}`);
            const data = await response.json();

            localStorage.setItem('jw-token', data.jw_token);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);

        const code = urlParams.get('code');
        const state = urlParams.get('state');

        console.log(state);

        if (code && state) {
            fetchToken(code, state);
        }

        router.push('/');
    });
    
    return <></>
}