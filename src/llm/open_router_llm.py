from openai import OpenAI
from typing import List, Dict, AsyncGenerator
from .llm_interface import LLMInterface

class OpenRouterLLM(LLMInterface):
    """
    An LLM implementation using the OpenRouter API via the OpenAI SDK.
    """

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model

    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Sends a chat request to the OpenRouter API and yields the response.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
        )

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content