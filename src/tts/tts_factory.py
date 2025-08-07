from .tts_interface import TTSInterface
from .dummy_tts import DummyTTS
from .edge_tts import EdgeTTS
from .chatterbox_tts import ChatterboxTTS
from .bark_tts import BarkTTS

class TTSFactory:
    @staticmethod
    def create_tts_engine(engine_name: str, **kwargs) -> TTSInterface:
        if engine_name == "dummy":
            return DummyTTS(**kwargs)
        elif engine_name == "edge_tts":
            voice = kwargs.pop('voice', 'en-US-AvaMultilingualNeural')
            return EdgeTTS(voice=voice, **kwargs)
        elif engine_name == "chatterbox_tts":
            return ChatterboxTTS(**kwargs)
        elif engine_name == "bark_tts":
            return BarkTTS(**kwargs)
        else:
            raise ValueError(f"Unknown TTS engine: {engine_name}")