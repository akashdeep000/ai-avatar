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
        model: str = "sense-voice",
        num_threads: int = 4,
        debug: bool = False,
        device: str = "cpu",
        compute_type: str = "int8",
        language: str = "",
    ) -> None:
        self.model_name = model
        self.num_threads = num_threads
        self.debug = debug
        self.device = device
        self.compute_type=compute_type
        self.language=language

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
        if self.model_name.startswith("whisper"):
            encoder_path, decoder_path, tokens_path = self._get_model_paths()
            return sherpa_onnx.OfflineRecognizer.from_whisper(
                encoder=encoder_path,
                decoder=decoder_path,
                tokens=tokens_path,
                num_threads=self.num_threads,
                debug=self.debug,
                provider=self.device,
                language=self.language,
                task="transcribe",
            )
        elif self.model_name == "sense-voice":
            model_path, tokens_path = self._get_model_paths()
            return sherpa_onnx.OfflineRecognizer.from_sense_voice(
                model=model_path,
                tokens=tokens_path,
                num_threads=self.num_threads,
                debug=self.debug,
                provider=self.device,
                language=self.language,
                use_itn=True,
            )
        else:
            raise ValueError(f"Unsupported model name: {self.model_name}")

    def _get_model_paths(self):
        model_path_dict = {
            # Sense Voice
            "sense-voice": "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17",

            # Whisper Models
            "whisper-tiny": "sherpa-onnx-whisper-tiny",
            "whisper-tiny.en": "sherpa-onnx-whisper-tiny.en",
            "whisper-base": "sherpa-onnx-whisper-base",
            "whisper-base.en": "sherpa-onnx-whisper-base.en",
            "whisper-small": "sherpa-onnx-whisper-small",
            "whisper-small.en": "sherpa-onnx-whisper-small.en",
            "whisper-medium": "sherpa-onnx-whisper-medium",
            "whisper-medium.en": "sherpa-onnx-whisper-medium.en",
            "whisper-large-v1": "sherpa-onnx-whisper-large-v1",
            "whisper-large-v2": "sherpa-onnx-whisper-large-v2",
            "whisper-large-v3": "sherpa-onnx-whisper-large-v3",

            # Whisper Distilled Models
            "whisper-distil-small.en": "sherpa-onnx-whisper-distil-small.en",
            "whisper-distil-medium.en": "sherpa-onnx-whisper-distil-medium.en",
            "whisper-distil-large-v2": "sherpa-onnx-whisper-distil-large-v2",

            # Other
            "whisper-medium-aishell": "sherpa-onnx-whisper-medium-aishell",
            "whisper-turbo": "sherpa-onnx-whisper-turbo",
        }

        if self.model_name not in model_path_dict:
            raise ValueError(f"Unsupported model name: {self.model_name}. Supported models are: {list(model_path_dict.keys())}")

        model_dir_name = model_path_dict[self.model_name]
        model_dir = f"./models/{model_dir_name}"

        if not os.path.exists(model_dir):
            logger.info(f"Model not found at {model_dir}. Downloading...")
            url = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{model_dir_name}.tar.bz2"
            output_dir = "./models"
            local_result = check_and_extract_local_file(url, output_dir)

            if local_result is None:
                logger.info("Local file not found. Downloading...")
                download_and_extract(url, output_dir)
            else:
                logger.info("Local file found. Using existing file.")

        if self.model_name.startswith("whisper"):
            prefix = self.model_name.replace("whisper-", "")

            encoder_path = os.path.join(model_dir, f"{prefix}-encoder.onnx")
            decoder_path = os.path.join(model_dir, f"{prefix}-decoder.onnx")

            if self.compute_type == "int8":
                int8_encoder_path = os.path.join(model_dir, f"{prefix}-encoder.int8.onnx")
                int8_decoder_path = os.path.join(model_dir, f"{prefix}-decoder.int8.onnx")
                if os.path.exists(int8_encoder_path):
                    encoder_path = int8_encoder_path
                if os.path.exists(int8_decoder_path):
                    decoder_path = int8_decoder_path

            tokens_path = os.path.join(model_dir, f"{prefix}-tokens.txt")
            return encoder_path, decoder_path, tokens_path
        else: # sense-voice
            return os.path.join(model_dir, "model.onnx"), os.path.join(model_dir, "tokens.txt")


    def transcribe_np(self, audio: np.ndarray) -> str:
        stream = self.recognizer.create_stream()
        stream.accept_waveform(16000, audio)
        self.recognizer.decode_streams([stream])
        return stream.result.text.strip()
