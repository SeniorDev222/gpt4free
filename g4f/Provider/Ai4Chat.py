from __future__ import annotations

from aiohttp import ClientSession
import re

from ..typing import AsyncResult, Messages
from .base_provider import AsyncGeneratorProvider, ProviderModelMixin
from .helper import format_prompt


class Ai4Chat(AsyncGeneratorProvider, ProviderModelMixin):
    url = "https://www.ai4chat.co"
    api_endpoint = "https://www.ai4chat.co/generate-response"
    working = True
    supports_gpt_4 = False
    supports_stream = False
    supports_system_message = True
    supports_message_history = True
    
    default_model = 'gpt-4'

    @classmethod
    def get_model(cls, model: str) -> str:
        return cls.default_model

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        model = cls.get_model(model)
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'cookie': 'messageCount=2',
            'origin': 'https://www.ai4chat.co',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.ai4chat.co/gpt/talkdirtytome',
            'sec-ch-ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        
        async with ClientSession(headers=headers) as session:
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": format_prompt(messages)
                    }
                ]
            }
            
            async with session.post(cls.api_endpoint, json=payload, proxy=proxy) as response:
                response.raise_for_status()
                response_data = await response.json()
                message = response_data.get('message', '')
                clean_message = re.sub('<[^<]+?>', '', message).strip()
                yield clean_message
