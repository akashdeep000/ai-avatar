import uuid
import os
import asyncio
from typing import Dict, List
from loguru import logger
import numpy as np

from .asr.asr_interface import ASRInterface
from .tts.tts_interface import TTSInterface
from .llm.llm_interface import LLMInterface
from .character_manager import Character, character_manager
from .live2d.live2d_model import Live2dModel
from .prompts import prompt_loader
from . import globals

class Session:
    def __init__(self, session_id: str, client_id: str):
        self.session_id: str = session_id
        self.client_id: str = client_id
        self.character: Character | None = None
        self.history: List[Dict[str, str]] = []
        self.live2d_model: Live2dModel | None = None

        # AI module instances
        self.asr_engine: ASRInterface | None = None
        self.tts_engine: TTSInterface | None = None
        self.llm_engine: LLMInterface | None = None
        self.asr_stream: "sherpa_onnx.OnlineStream" | None = None
        self.active_llm_task: asyncio.Task | None = None
        self.last_asr_text: str = ""
        self.audio_buffer = bytearray()
        self.interrupted: bool = False

    def initialize_modules(self, character_id: str):
        self.character = character_manager.get_character(character_id)
        if not self.character:
            raise ValueError(f"Character '{character_id}' not found.")

        self.live2d_model = Live2dModel(
            live2d_model_name=self.character.live2d_model_name,
            model_dict_path="model_dict.json"
        )

        # Assign pre-loaded engines from globals
        self.asr_engine = globals.asr_engine
        self.llm_engine = globals.llm_engine
        if self.character.id in globals.tts_engines:
            self.tts_engine = globals.tts_engines[self.character.id]
        else:
            logger.error(f"TTS engine for character '{self.character.id}' not found in pre-loaded engines.")
            # As a fallback, you might want to load it on-demand or raise an error
            # For now, we'll leave it as None and let it fail downstream
            self.tts_engine = None

        # Initialize conversation history with the character's persona
        try:
            # Load and format expression prompt
            expression_prompt_template = prompt_loader.load_util("live2d_expression_prompt")
            expression_prompt = expression_prompt_template.replace(
                "[<insert_emomap_keys>]", self.live2d_model.emo_str
            )
        except Exception as e:
            logger.error(f"Error loading expression prompt, falling back to default: {e}")
            expression_prompt = f"You can use the following expressions: {self.live2d_model.emo_str}"

        try:
            # Load and format motion prompt
            motion_prompt_template = prompt_loader.load_util("live2d_motion_prompt")
            motion_prompt = motion_prompt_template.replace(
                "[<insert_motion_keys>]", self.live2d_model.motion_str
            )
        except Exception as e:
            logger.error(f"Error loading motion prompt, falling back to default: {e}")
            motion_prompt = f"You can use the following motions: {self.live2d_model.motion_str}"

        speakable_prompt = prompt_loader.load_util("speakable_prompt")
        concise_style_prompt = prompt_loader.load_util("concise_style_prompt")

        system_prompt = f"{self.character.llm_persona}\n\n{speakable_prompt}\n\n{expression_prompt}\n\n{motion_prompt}\n\n{concise_style_prompt}"

        self.history.append({"role": "system", "content": system_prompt})
        logger.info(f"Initialized AI modules for session {self.session_id} with character {self.character.name}")


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self, client_id: str) -> Session:
        if client_id in self.sessions:
            return self.sessions[client_id]

        session_id = str(uuid.uuid4())
        session = Session(session_id, client_id)
        self.sessions[client_id] = session
        logger.info(f"Created session {session_id} for client {client_id}")
        return session

    def get_session(self, client_id: str) -> Session | None:
        return self.sessions.get(client_id)

    def remove_session(self, client_id: str):
        if client_id in self.sessions:
            session_id = self.sessions[client_id].session_id
            del self.sessions[client_id]
            logger.info(f"Removed session {session_id} for client {client_id}")

session_manager = SessionManager()