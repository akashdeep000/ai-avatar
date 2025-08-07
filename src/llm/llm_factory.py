from .llm_interface import LLMInterface
from .dummy_llm import DummyLLM
from .open_router_llm import OpenRouterLLM
from .google_gemini_llm import GoogleGeminiLLM

class LLMFactory:
    @staticmethod
    def create_llm_engine(engine_name: str, **kwargs) -> LLMInterface:
        if engine_name == "dummy":
            return DummyLLM(**kwargs)
        elif engine_name == "open_router":
            return OpenRouterLLM(**kwargs)
        elif engine_name == "google_gemini":
            return GoogleGeminiLLM(**kwargs)
        else:
            raise ValueError(f"Unknown LLM engine: {engine_name}")