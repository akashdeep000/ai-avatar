from loguru import logger
import json
import os
from typing import Dict, List

class Live2dModel:
    def __init__(self, live2d_model_name: str, model_dict_path: str = "model_dict.json"):
        self.model_dict_path = model_dict_path
        self.live2d_model_name = live2d_model_name
        self.model_info: Dict = {}
        self.emo_map: Dict = {}
        self.motion_map: Dict = {}
        self.motion_groups: Dict = {}
        self.emo_str: str = ""
        self.motion_str: str = ""
        self.set_model(live2d_model_name)

    def set_model(self, model_name: str) -> None:
        self.model_info = self._lookup_model_info(model_name)

        # Load emotion map
        self.emo_map = {
            k.lower(): v for k, v in self.model_info.get("emotionMap", {}).items()
        }
        self.emo_str = " ".join([f"[e:{key}]" for key in self.emo_map.keys()])

        # Load motion map
        self.motion_map = {
            k.lower(): v for k, v in self.model_info.get("motionMap", {}).items()
        }
        self.motion_str = " ".join([f"[m:{key}]" for key in self.motion_map.keys()])

        # Dynamically load motion groups from the model's .model3.json file
        self._load_motion_groups()

    def _load_motion_groups(self):
        model3_json_path = self.model_info.get("url")
        if not model3_json_path:
            return

        # The path in model_dict is relative to the frontend, so we need to construct the correct path for the backend
        # Assumes the live2d-models directory is at the same level as where the script is run
        backend_path = os.path.join("live2d-models", self.live2d_model_name, "runtime", os.path.basename(model3_json_path))

        # A more robust way might be to have a base path config, but this works for the current structure
        if not os.path.exists(backend_path):
             # try another path
             backend_path = os.path.join("ai-avatar-service", "live2d-models", self.live2d_model_name, "runtime", os.path.basename(model3_json_path))
             if not os.path.exists(backend_path):
                  logger.warning(f"Warning: {backend_path} not found. Cannot load motion groups.")
                  return

        with open(backend_path, 'r', encoding='utf-8') as f:
            model_config = json.load(f)

        self.motion_groups = model_config.get("FileReferences", {}).get("Motions", {})


    def _lookup_model_info(self, model_name: str) -> Dict:
        with open(self.model_dict_path, 'r', encoding='utf-8') as f:
            model_dict = json.load(f)

        matched_model = next((model for model in model_dict if model["name"] == model_name), None)

        if matched_model is None:
            raise KeyError(f"{model_name} not found in model dictionary {self.model_dict_path}.")

        return matched_model