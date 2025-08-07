from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file='.env', extra='ignore')

    LLM_ENGINE: str = Field(default="open_router", description="LLM engine to use.")
    LLM_MODEL: str = Field(default="z-ai/glm-4.5-air:free", description="LLM model to use.")
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, description="OpenRouter API key.")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API key.")

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='APP_', case_sensitive=False, env_file='.env', extra='ignore')

    ASR_ENGINE: str = Field(default="sherpa_onnx_asr", description="ASR engine to use. Options: 'sherpa_onnx_asr', 'faster_whisper_asr'")
    ASR_DEVICE: str = Field(default="cpu", description="Device for ASR inference, e.g., 'cpu', 'cuda'")
    TTS_DEVICE: str = Field(default="cpu", description="Device for TTS inference, e.g. cpu, cuda")
    ALLOWED_ORIGINS: str = Field(default="*", description="Allowed origins for CORS, comma-separated. Use '*' for all.")

app_config = AppConfig()
llm_config = LLMConfig()