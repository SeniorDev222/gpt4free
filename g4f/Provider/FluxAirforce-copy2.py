from __future__ import annotations

from aiohttp import ClientSession
from urllib.parse import urlencode

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..image import ImageResponse

class FluxAirforce(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://flux.api.airforce/"
    api_endpoint = "https://api.airforce/v1/imagine2"
    working = True
    default_model = 'flux-realism'
    models = [
        'flux',
        'flux-realism',
        'flux-anime',
        'flux-3d',
        'flux-disney'
    ]

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://flux.api.airforce",
            "priority": "u=1, i",
            "referer": "https://flux.api.airforce/",
            "sec-ch-ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }

        prompt = messages[-1]['content'] if messages else ""

        params = {
            "prompt": prompt,
            "size": kwargs.get("size", "1:1"),
            "seed": kwargs.get("seed"),
            "model": model
        }

        params = {k: v for k, v in params.items() if v is not None}

        async with ClientSession(headers=headers) as session:
            async with session.get(f"{cls.api_endpoint}", params=params, proxy=proxy) as response:
                response.raise_for_status()
                image_url = str(response.url)
                yield ImageResponse(image_url, prompt)
