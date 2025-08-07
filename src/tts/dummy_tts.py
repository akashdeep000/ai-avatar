from loguru import logger
from .tts_interface import TTSInterface

class DummyTTS(TTSInterface):
    """
    A dummy TTS implementation for testing purposes.
    It does not perform any actual speech synthesis.
    """

    async def synthesize(self, text: str) -> bytes:
        """
        Returns empty bytes, simulating synthesized audio.

        Args:
            text: The text to synthesize (ignored).

        Returns:
            An empty bytes object.
        """
        logger.debug(f"DummyTTS: Synthesizing text: '{text}' (returning empty audio).")
        return b""