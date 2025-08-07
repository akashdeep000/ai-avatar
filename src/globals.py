from typing import Dict
from .asr.asr_interface import ASRInterface
from .llm.llm_interface import LLMInterface
from .tts.tts_interface import TTSInterface

# Global instances for AI modules
asr_engine: ASRInterface | None = None
llm_engine: LLMInterface | None = None
tts_engines: Dict[str, TTSInterface] = {}