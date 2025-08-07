from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator

class LLMInterface(ABC):
    """
    Abstract base class for Large Language Model services.
    """

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Sends a chat request to the LLM and yields the response.

        Args:
            messages: A list of messages in the conversation history.
            stream: Whether to stream the response or not.

        Yields:
            The response from the LLM as a string.
        """
        yield "This is a placeholder response."