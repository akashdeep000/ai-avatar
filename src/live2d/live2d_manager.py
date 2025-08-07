import os
from fastapi import HTTPException

class Live2DManager:
    def __init__(self, models_dir: str = "live2d-models"):
        self.models_dir = models_dir

    def get_model_path(self, model_name: str) -> str:
        """
        Constructs the path to a Live2D model's main JSON file.

        Args:
            model_name: The name of the model (directory name).

        Returns:
            The path to the model's .model3.json file.

        Raises:
            HTTPException: If the model directory or file does not exist.
        """
        model_dir = os.path.join(self.models_dir, model_name)
        if not os.path.isdir(model_dir):
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")

        model_file = os.path.join(model_dir, "runtime", f"{model_name}.model3.json")
        if not os.path.isfile(model_file):
            raise HTTPException(status_code=404, detail=f"Model file for '{model_name}' not found.")

        return model_file

live2d_manager = Live2DManager()