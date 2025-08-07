from abc import ABC, abstractmethod

class TTSInterface(ABC):
    """
    Abstract base class for Text-to-Speech services.
    """

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """
        Synthesizes the given text into audio data.

        Args:
            text: The text to synthesize.

        Returns:
            A bytes object containing the audio data.
        """
        pass