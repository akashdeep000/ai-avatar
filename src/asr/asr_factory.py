from .sherpa_onnx_asr import SherpaOnnxASR
from .faster_whisper_asr import FasterWhisperASR
from .asr_interface import ASRInterface

class ASRFactory:
    @staticmethod
    def get_asr_system(name: str, **kwargs) -> ASRInterface:
        if name == "sherpa_onnx_asr":
            return SherpaOnnxASR(**kwargs)
        elif name == "faster_whisper_asr":
            return FasterWhisperASR(**kwargs)
        else:
            raise ValueError(f"Unknown ASR system: {name}")