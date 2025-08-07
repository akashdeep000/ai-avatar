import io
import os
import platform
from bark import SAMPLE_RATE, generate_audio, preload_models
from loguru import logger
from scipy.io.wavfile import write as write_wav
from .tts_interface import TTSInterface

class BarkTTS(TTSInterface):
    def __init__(self, voice="v2/en_speaker_1"):
        os.environ["SUNO_USE_SMALL_MODELS"] = "True"
        if platform.system() == "Darwin":
            logger.info(">> Note: Running barkTTS on macOS can be very slow.")
            os.environ["SUNO_ENABLE_MPS"] = "True"
            os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
            os.environ["SUNO_OFFLOAD_CPU"] = "False"

        # download and load all models
        preload_models()
        self.voice = voice

    async def synthesize(self, text: str) -> bytes:
        """
        Generate speech audio file using TTS.
        text: str
            the text to speak

        Returns:
        bytes: the generated audio data

        """
        try:
            # generate audio from text
            audio_array = generate_audio(text, history_prompt=self.voice)

            # save audio to a bytes buffer
            buffer = io.BytesIO()
            write_wav(filename=buffer, rate=SAMPLE_RATE, data=audio_array)
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            logger.critical(f"\nError: bark-tts unable to generate audio: {e}")
            return b""