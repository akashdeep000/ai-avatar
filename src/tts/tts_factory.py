from .tts_interface import TTSInterface
from .dummy_tts import DummyTTS
from .edge_tts import EdgeTTS
from .chatterbox_tts import ChatterboxTTS
from src.config import chatterbox_tts_config

class TTSFactory:
    @staticmethod
    def create_tts_engine(engine_name: str, **kwargs) -> TTSInterface:
        if engine_name == "dummy":
            return DummyTTS(**kwargs)
        elif engine_name == "edge_tts":
            voice = kwargs.pop('voice', 'en-US-AvaMultilingualNeural')
            return EdgeTTS(voice=voice, **kwargs)
        elif engine_name == "chatterbox_tts":
            kwargs['base_url'] = chatterbox_tts_config.BASE_URL
            kwargs['api_key'] = chatterbox_tts_config.API_KEY
            return ChatterboxTTS(**kwargs)
        else:
            raise ValueError(f"Unknown TTS engine: {engine_name}")