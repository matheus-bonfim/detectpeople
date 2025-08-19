import httpx
import asyncio
from typing import Optional
import json

class AsyncHTTPClient:
    def __init__(self, base_url: Optional[str] = None, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def get(self, url: str, params: dict = None, headers: dict = None):
        try:
            response = await self.client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Erro de status: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Erro de requisição: {str(e)}")
        return None

    async def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None):
        try:
            response = await self.client.post(url, data=data, json=json, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Erro de status: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Erro de requisição: {str(e)}")
        return None

    async def close(self):
        await self.client.aclose()

# Uso típico

client = AsyncHTTPClient(base_url='http://localhost:3500/api')

async def notify(data):
    await client.post("/notify", json=data)
   


