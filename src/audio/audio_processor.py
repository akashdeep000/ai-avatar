import numpy as np
from loguru import logger
import noisereduce as nr
import pyloudnorm as pyln
from scipy.signal import butter, lfilter
from ..config import app_config

class AudioProcessor:
    def _band_pass_filter(self, data, sample_rate, lowcut=300.0, highcut=3400.0, order=5):
        nyquist = 0.5 * sample_rate
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    def process(self, audio_np: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
        """
        Applies the configured audio processing pipeline to the audio data.
        """
        if not app_config.ENABLE_AUDIO_PROCESSING:
            return audio_np

        processed_audio = audio_np

        if app_config.NOISE_REDUCTION:
            try:
                processed_audio = nr.reduce_noise(y=processed_audio, sr=sample_rate)
            except Exception as e:
                logger.warning(f"Failed to apply noise reduction: {e}")

        if app_config.LOUDNESS_NORMALIZATION:
            try:
                meter = pyln.Meter(sample_rate)
                loudness = meter.integrated_loudness(processed_audio)
                processed_audio = pyln.normalize.loudness(processed_audio, loudness, -23.0)
            except Exception as e:
                logger.warning(f"Failed to apply loudness normalization: {e}")

        return processed_audio