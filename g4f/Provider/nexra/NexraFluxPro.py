from __future__ import annotations

import json
import requests
from ...typing import CreateResult, Messages
from ..base_provider import ProviderModelMixin, AbstractProvider
from ...image import ImageResponse

class NexraFluxPro(AbstractProvider, ProviderModelMixin):
    url = "https://nexra.aryahcr.cc/documentation/flux-pro/en"
    api_endpoint = "https://nexra.aryahcr.cc/api/image/complements"
    working = True
    
    default_model = 'flux'
    models = [default_model]
    model_aliases = {
        "flux-pro": "flux",
    }

    @classmethod
    def get_model(cls, model: str) -> str:
        if model in cls.models:
            return model
        elif model in cls.model_aliases:
            return cls.model_aliases[model]
        else:
            return cls.default_model
            
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        response: str = "url",  # base64 or url
        **kwargs
    ) -> CreateResult:
        model = cls.get_model(model)

        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "prompt": messages[-1]["content"],
            "model": model,
            "response": response
        }
        
        response = requests.post(cls.api_endpoint, headers=headers, json=data)

        result = cls.process_response(response)
        yield result

    @classmethod
    def process_response(cls, response):
        if response.status_code == 200:
            try:
                content = response.text.strip()
                content = content.lstrip('_')
                data = json.loads(content)
                if data.get('status') and data.get('images'):
                    image_url = data['images'][0]
                    return ImageResponse(images=[image_url], alt="Generated Image")
                else:
                    return "Error: No image URL found in the response"
            except json.JSONDecodeError as e:
                return f"Error: Unable to decode JSON response. Details: {str(e)}"
        else:
            return f"Error: {response.status_code}, Response: {response.text}"
