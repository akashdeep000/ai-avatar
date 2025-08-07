from faster_whisper import WhisperModel
import numpy as np
from .asr_interface import ASRInterface

class FasterWhisperASR(ASRInterface):
    def __init__(self, model_size="distil-small.en", device="cpu", compute_type="default"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_data: np.ndarray, sample_rate: int) -> str:
        segments, _ = self.model.transcribe(audio_data, beam_size=5)
        return " ".join([segment.text for segment in segments])

    def transcribe_np(self, audio_np: np.ndarray) -> str:
        # faster-whisper works on the full audio, so we just transcribe it directly
        # This implementation is not streaming, it will re-transcribe the whole buffer every time.
        # For a production scenario, a more sophisticated streaming implementation would be needed.
        segments, _ = self.model.transcribe(audio_np)
        return " ".join([segment.text for segment in segments])