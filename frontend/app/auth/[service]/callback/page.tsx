'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Page({
    params,
    searchParams
}: {
    params: { service: string },
    searchParams: { [key: string]: string | string[] | undefined }
}) {
    const router = useRouter();

    const fetchToken = async (code: string, state: string) => {
        try {
            const urlParams = new URLSearchParams();
            urlParams.append('code', code);
            urlParams.append('state', state);

            const url = new URL(`http://127.0.0.1:8000/v1/auth/${params.service}/callback`);
            url.search = urlParams.toString();

            const response = await fetch(url);
            const data = await response.json();

            localStorage.setItem(`${params.service}_token`, data.jw_token);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        if (params.service === 'google' || params.service === 'spotify') {
            if (typeof searchParams.code === 'string' && typeof searchParams.state === 'string') {
                fetchToken(searchParams.code, searchParams.state);
            }
        }

        router.push('/');
    });

    return <></>;
}