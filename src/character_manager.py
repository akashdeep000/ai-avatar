from loguru import logger
import yaml
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Character:
    id: str
    name: str
    llm_persona: str
    live2d_model_name: str
    motion_map: Dict[str, str]
    asr_engine: Dict[str, Any]
    tts_engine: Dict[str, Any]
    extra_data: Dict[str, Any]

class CharacterManager:
    def __init__(self, characters_dir: str = "characters"):
        self.characters: Dict[str, Character] = {}
        self.characters_dir = characters_dir
        self._load_characters()

    def _load_characters(self):
        if not os.path.isdir(self.characters_dir):
            logger.warning(f"Characters directory '{self.characters_dir}' not found. Creating it.")
            os.makedirs(self.characters_dir)
            return

        for filename in os.listdir(self.characters_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(self.characters_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        config = yaml.safe_load(f)
                        char_id = filename.split('.')[0]
                        character = Character(
                            id=char_id,
                            name=config.get("name", "Unknown"),
                            llm_persona=config.get("llm_persona", ""),
                            live2d_model_name=config.get("live2d_model_name", ""),
                            motion_map=config.get("motion_map", {}),
                            asr_engine=config.get("asr_engine", {}),
                            tts_engine=config.get("tts_engine", {}),
                            extra_data=config.get("extra_data", {})
                        )
                        self.characters[char_id] = character
                        logger.info(f"Loaded character: {character.name}")
                    except yaml.YAMLError as e:
                        logger.error(f"Error loading character from {filename}: {e}")

    def get_character(self, character_id: str) -> Character | None:
        return self.characters.get(character_id)

    def list_characters(self) -> List[Character]:
        return list(self.characters.values())

character_manager = CharacterManager(characters_dir="characters")