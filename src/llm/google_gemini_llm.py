import google.generativeai as genai
from typing import List, Dict, AsyncGenerator
from .llm_interface import LLMInterface

class GoogleGeminiLLM(LLMInterface):
    """
    An LLM implementation using the Google Gemini API.
    """

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Sends a chat request to the Gemini API and yields the response.
        """
        system_prompt = next((msg["content"] for msg in messages if msg["role"] == "system"), "")

        # Adapt messages to the format expected by the Gemini API.
        # The role 'assistant' should be mapped to 'model'.
        gemini_messages = []
        is_first_user_message = True
        for msg in messages:
            role = msg["role"]
            if role == "assistant":
                role = "model"

            if role == "user":
                content = msg["content"]
                if is_first_user_message and system_prompt:
                    content = f"{system_prompt}\n\n{content}"
                    is_first_user_message = False
                gemini_messages.append({"role": role, "parts": [content]})
            elif role == "model":
                gemini_messages.append({"role": role, "parts": [msg["content"]]})

        response = self.model.generate_content(
            gemini_messages,
            stream=stream,
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
            },
        )

        if stream:
            for chunk in response:
                yield chunk.text
        else:
            yield response.text