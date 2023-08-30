'use client';

import { useEffect } from 'react';

const BACKEND_URL = process.env.BACKEND_URL;

export default function Page({
    params,
    searchParams
}: {
    params: { service: string },
    searchParams: { [key: string]: string | string[] | undefined }
}) {
    const fetchToken = async (code: string, state: string) => {
        try {
            const urlParams = new URLSearchParams();
            urlParams.append('code', code);
            urlParams.append('state', state);

            const url = new URL(`${BACKEND_URL}/v1/auth/${params.service}/callback`);
            url.search = urlParams.toString();

            const response = await fetch(url);
            const data = await response.json();

            localStorage.setItem(`${params.service}_token`, data.jwt);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        const handleTokenAndNavigate = async () => {
            if (params.service === 'google' || params.service === 'spotify') {
              if (typeof searchParams.code === 'string' && typeof searchParams.state === 'string') {
                await fetchToken(searchParams.code, searchParams.state);
              }
            }
            
            window.close();
          };
      
          handleTokenAndNavigate();
    }, []);

    return <></>;
}