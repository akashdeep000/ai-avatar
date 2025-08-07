from typing import List, Dict, AsyncGenerator
import asyncio
from .llm_interface import LLMInterface

class DummyLLM(LLMInterface):
    """
    A dummy LLM implementation for testing purposes.
    """

    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Yields a fixed, dummy response.
        """
        response = "This is a dummy response from the LLM. It is not real."
        if stream:
            for char in response:
                yield char
        else:
            yield response