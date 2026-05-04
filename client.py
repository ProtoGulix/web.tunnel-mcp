import os
import httpx
from dotenv import load_dotenv

load_dotenv()

_BASE_URL = os.environ.get("TUNNEL_API_BASE_URL", "http://localhost:8000")
_TOKEN = os.environ.get("TUNNEL_API_TOKEN", "")


class TunnelClient:
    def __init__(self):
        self._base_url = _BASE_URL.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"X-API-Key": _TOKEN},
            timeout=15.0,
        )

    async def get(self, path: str, params: dict = None) -> dict:
        response = await self._client.get(path, params=params)
        if response.status_code >= 400:
            raise RuntimeError(
                f"API error {response.status_code} on GET {path}: {response.text}"
            )
        return response.json()

    async def aclose(self):
        await self._client.aclose()


tunnel_client = TunnelClient()
