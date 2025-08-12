from loguru import logger
import httpx
from .tts_interface import TTSInterface
from typing import Optional, Any, Dict

class ChatterboxTTS(TTSInterface):
    """
    A TTS implementation for the custom Chatterbox TTS service.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, **kwargs):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["X-API-Key"] = api_key

        self.tts_params: Dict[str, Any] = kwargs
        if 'voice' in self.tts_params:
            self.tts_params['voice_id'] = self.tts_params.pop('voice')


    async def synthesize(self, text: str) -> bytes:
        """
        Synthesizes the given text into audio data by calling the Chatterbox API.

        Args:
            text: The text to synthesize.

        Returns:
            A bytes object containing the audio data.
        """
        url = f"{self.base_url}/tts/generate"
        payload = {
            "text": text,
            **self.tts_params
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.content
            except httpx.RequestError as e:
                logger.error(f"An error occurred while requesting {e.request.url!r}.")
                return b""
            except httpx.HTTPStatusError as e:
                logger.error(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
                return b""