import edge_tts
from .tts_interface import TTSInterface

class EdgeTTS(TTSInterface):
    """
    A TTS implementation using Microsoft Edge's online TTS service.
    """

    def __init__(self, voice: str = "en-US-AriaNeural"):
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        """
        Synthesizes the given text into audio data using edge-tts.

        Args:
            text: The text to synthesize.

        Returns:
            A bytes object containing the audio data in raw PCM format.
        """
        communicate = edge_tts.Communicate(text, self.voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data