from abc import ABC, abstractmethod
import numpy as np

class ASRInterface(ABC):
    @abstractmethod
    def transcribe_np(self, audio: np.ndarray) -> str:
        pass