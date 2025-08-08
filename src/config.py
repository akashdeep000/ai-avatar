from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file='.env', extra='ignore')

    LLM_ENGINE: str = Field(default="open_router", description="LLM engine to use.")
    LLM_MODEL: str = Field(default="z-ai/glm-4.5-air:free", description="LLM model to use.")
    OPENROUTER_API_KEY: Optional[str] = Field(default=None, description="OpenRouter API key.")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API key.")

class ASRConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ASR_', case_sensitive=False, env_file='.env', extra='ignore')

    ENGINE: str = Field(default="sherpa_onnx_asr", description="ASR engine to use. Options: 'sherpa_onnx_asr', 'faster_whisper_asr'")
    DEVICE: str = Field(default="cpu", description="Device for ASR inference, e.g., 'cpu', 'cuda', auto")
    MODEL: str = Field(default="whisper-distil-small.en", description="Model for Faster Whisper ASR or Model for Sherpa.")
    COMPUTE_TYPE: str = Field(default="int8", description="Compute type for Faster Whisper ASR.")
    CPU_THREADS: int = Field(default=4, description="Number of CPU threads for ASR.")

class TTSConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TTS_', case_sensitive=False, env_file='.env', extra='ignore')

    DEVICE: str = Field(default="cpu", description="Device for TTS inference, e.g. cpu, cuda")

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='APP_', case_sensitive=False, env_file='.env', extra='ignore')

    ALLOWED_ORIGINS: str = Field(default="*", description="Allowed origins for CORS, comma-separated. Use '*' for all.")

app_config = AppConfig()
llm_config = LLMConfig()
asr_config = ASRConfig()
tts_config = TTSConfig()