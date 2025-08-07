import os
import numpy as np
import sherpa_onnx
from loguru import logger
from .asr_interface import ASRInterface
from .utils import download_and_extract, check_and_extract_local_file
import onnxruntime


class SherpaOnnxASR(ASRInterface):
    def __init__(
        self,
        num_threads: int = 1,
        debug: bool = False,
        device: str = "cpu",
    ) -> None:
        self.num_threads = num_threads
        self.debug = debug
        self.device = device

        if self.device == "cuda":
            try:
                if "CUDAExecutionProvider" not in onnxruntime.get_available_providers():
                    logger.warning(
                        "CUDA provider not available for ONNX. Falling back to CPU."
                    )
                    self.device = "cpu"
            except ImportError:
                logger.warning("ONNX Runtime not installed. Falling back to CPU.")
                self.device = "cpu"
        logger.info(f"Sherpa-Onnx-ASR: Using {self.device} for inference")

        self.recognizer = self._create_recognizer()

    def _create_recognizer(self):
        model_path, tokens_path = self._get_model_paths()

        model_path, tokens_path = self._get_model_paths()

        return sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=model_path,
            tokens=tokens_path,
            num_threads=self.num_threads,
            debug=self.debug,
            provider=self.device,
            use_itn=False,
        )

    def _get_model_paths(self) -> (str, str):
        model_dir = "./models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
        model_path = os.path.join(model_dir, "model.onnx")
        tokens_path = os.path.join(model_dir, "tokens.txt")

        if not os.path.exists(model_path):
            logger.info(f"SenseVoice model not found at {model_dir}. Downloading...")
            url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2"
            output_dir = "./models"
            local_result = check_and_extract_local_file(url, output_dir)

            if local_result is None:
                logger.info("Local file not found. Downloading...")
                download_and_extract(url, output_dir)
            else:
                logger.info("Local file found. Using existing file.")

        return model_path, tokens_path

    def transcribe_np(self, audio: np.ndarray) -> str:
        stream = self.recognizer.create_stream()
        stream.accept_waveform(16000, audio)
        self.recognizer.decode_streams([stream])
        return stream.result.text.strip()
