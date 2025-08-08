import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import sys
import base64
import asyncio
from contextlib import asynccontextmanager
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from io import BytesIO
import wave
from fastapi.responses import HTMLResponse, JSONResponse
import os
from dotenv import load_dotenv
import time

load_dotenv()

from .config import app_config, llm_config, asr_config, tts_config
from .connection_manager import manager
from .session_manager import session_manager, Session
from .character_manager import character_manager
from .utils.actions_extractor import extract_actions
from .utils.sentence_splitter import split_sentences
from . import globals
from .asr.asr_factory import ASRFactory
from .llm.llm_factory import LLMFactory
from .tts.tts_factory import TTSFactory
from loguru import logger
from .audio.audio_processor import AudioProcessor

def _load_models_sync():
    """
    Synchronously loads all AI models. This function is designed to be run in a
    separate thread to avoid blocking the main asyncio event loop.
    """
    logger.info("Loading AI models in a background thread...")

    # Load ASR engine
    try:
        globals.asr_engine = ASRFactory.get_asr_system(
            asr_config.ENGINE,
            device=asr_config.DEVICE,
            model=asr_config.MODEL,
            compute_type=asr_config.COMPUTE_TYPE,
            num_threads=asr_config.CPU_THREADS
        )
        logger.info("ASR engine loaded.")
    except Exception as e:
        logger.error(f"Failed to load ASR engine: {e}")

    # Load LLM engine
    try:
        api_key = None
        if llm_config.LLM_ENGINE == "open_router":
            api_key = llm_config.OPENROUTER_API_KEY
        elif llm_config.LLM_ENGINE == "google_gemini":
            api_key = llm_config.GEMINI_API_KEY
        globals.llm_engine = LLMFactory.create_llm_engine(
            llm_config.LLM_ENGINE,
            api_key=api_key,
            model=llm_config.LLM_MODEL
        )
        logger.info("LLM engine loaded.")
    except Exception as e:
        logger.error(f"Failed to load LLM engine: {e}")

    # Load TTS engines for all characters
    characters = character_manager.list_characters()
    for character in characters:
        if character:
            try:
                tts_engine_config = character.tts_engine.copy()
                tts_engine_name = tts_engine_config.pop("name")
                tts_engine = TTSFactory.create_tts_engine(tts_engine_name, **tts_engine_config)
                globals.tts_engines[character.id] = tts_engine
                logger.info(f"TTS engine for character '{character.name}' loaded.")
            except Exception as e:
                logger.error(f"Failed to load TTS engine for character '{character.name}': {e}")

    logger.info("All AI models loaded.")

async def load_models_async():
    """
    Triggers the synchronous model loading function in a separate thread.
    """
    await asyncio.to_thread(_load_models_sync)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        "logs/app.log",
        level="INFO",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        compression="zip",
        serialize=True,  # This enables JSON output
    )

    # Start model loading in a background task
    asyncio.create_task(load_models_async())

    yield

    # Clean up resources if needed on shutdown
    logger.info("Application shutting down.")


app = FastAPI(lifespan=lifespan)
audio_processor = AudioProcessor()

if app_config.ALLOWED_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in app_config.ALLOWED_ORIGINS.split(',')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def liveness_check():
    """A simple check to see if the service is alive."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """
    Checks if the service is ready to serve requests by verifying that all models are loaded.
    """
    unloaded_models = []
    if not globals.asr_engine:
        unloaded_models.append("ASR")
    if not globals.llm_engine:
        unloaded_models.append("LLM")
    if not globals.tts_engines:
        unloaded_models.append("TTS")

    if unloaded_models:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": f"The following models are not loaded: {', '.join(unloaded_models)}"}
        )

    return {"status": "ok"}

@app.get("/characters")
async def list_characters():
    all_characters = character_manager.list_characters()
    available_characters = [
        char for char in all_characters if char.id in globals.tts_engines
    ]
    return {"characters": available_characters}

app.mount("/live2d-models", StaticFiles(directory="live2d-models"), name="live2d-models")

async def handle_text_message(session: Session, text: str):
    session.history.append({"role": "user", "content": text})
    session.interrupted = False

    llm_response_text = ""
    llm_stream = session.llm_engine.chat(session.history, stream=True)

    sentence_buffer = ""
    first_sentence_processed = False
    try:
        async for chunk in llm_stream:
            if session.interrupted:
                logger.info("LLM stream processing interrupted.")
                break

            llm_response_text += chunk
            sentence_buffer += chunk

            sentences = split_sentences(sentence_buffer, faster_first_response=not first_sentence_processed)

            if sentences:
                for i, sentence in enumerate(sentences):
                    if i < len(sentences) - 1:
                        if sentence.strip():
                            await process_sentence(session, sentence)
                            first_sentence_processed = True

                sentence_buffer = sentences[-1]

        if len(sentence_buffer.strip()) > 0 and not session.interrupted:
            await process_sentence(session, sentence_buffer)

    except asyncio.CancelledError:
        logger.info("LLM stream cancelled.")
    finally:
        if llm_response_text:
            session.history.append({"role": "assistant", "content": llm_response_text})
        # Signal that the LLM response is complete
        await manager.send_personal_message(json.dumps({"type": "avatar:idle"}), session.client_id)
        session.active_llm_task = None

async def process_sentence(session: Session, sentence: str):
    text_to_speak, expressions, motions = extract_actions(
        sentence,
        list(session.live2d_model.emo_map.keys()),
        list(session.live2d_model.motion_map.keys())
    )

    expression_data = [session.live2d_model.emo_map.get(exp) for exp in expressions if session.live2d_model.emo_map.get(exp)]
    motion_data = [session.live2d_model.motion_map.get(mot) for mot in motions if session.live2d_model.motion_map.get(mot)]

    audio_base64 = ""
    if text_to_speak.strip():
        tts_audio = await session.tts_engine.synthesize(text_to_speak)
        audio_base64 = base64.b64encode(tts_audio).decode('utf-8')

    if text_to_speak.strip() or expression_data or motion_data:
        playback_payload = {
            "type": "avatar:speak",
            "payload": {
                "text": text_to_speak,
                "audio": audio_base64,
                "expressions": expression_data,
                "motions": motion_data
            }
        }
        await manager.send_personal_message(json.dumps(playback_payload), session.client_id)

async def handle_session_start(session: Session, payload: dict):
    session.initialize_modules(payload["character_id"])
    response = {
        "type": "session:ready",
        "payload": {
            "session_id": session.session_id,
            "character": session.character.dict() if hasattr(session.character, 'dict') else session.character.__dict__,
            "live2d_model_info": session.live2d_model.model_info
        }
    }
    await manager.send_personal_message(json.dumps(response), session.client_id)

async def handle_user_text(session: Session, payload: dict):
    if session.active_llm_task:
        session.active_llm_task.cancel()
    session.active_llm_task = asyncio.create_task(handle_text_message(session, payload["text"]))

async def handle_user_interrupt(session: Session, payload: dict):
    session.interrupted = True
    if session.active_llm_task:
        session.active_llm_task.cancel()
        logger.info("LLM task interrupted by client.")
    session.last_asr_text = "" # Clear any partial transcription

async def handle_user_audio_chunk(session: Session, payload: dict):
    if session.asr_engine:
        audio_bytes = base64.b64decode(payload["data"])
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        audio_process_start_time = time.time()
        processed_audio_np = audio_processor.process(audio_np, 16000)
        logger.info(f"Audio processing took {time.time() - audio_process_start_time} seconds")

        if app_config.DEBUG_SAVE_AUDIO:
            if not os.path.exists("audio_debug"):
                os.makedirs("audio_debug")
            timestamp = int(time.time())
            sf.write(f"audio_debug/{timestamp}_original.wav", audio_np, 16000)
            sf.write(f"audio_debug/{timestamp}_processed.wav", processed_audio_np, 16000)

        audio_np = processed_audio_np

        asr_start_time = time.time()
        partial_text = session.asr_engine.transcribe_np(audio_np)
        logger.info(f"ASR transcribe took {time.time() - asr_start_time} seconds")

        # Implicit interruption ("barge-in")
        # Only interrupt if we get actual text from ASR and a task is active
        if partial_text and session.active_llm_task and not session.interrupted:
            session.active_llm_task.cancel()
            session.interrupted = True
            logger.info("LLM task interrupted by user speech (barge-in).")
        if session.last_asr_text:
            session.last_asr_text += " " + partial_text
        else:
            session.last_asr_text = partial_text

        response = {"type": "asr:partial", "payload": {"text": session.last_asr_text}}
        await manager.send_personal_message(json.dumps(response), session.client_id)

async def handle_user_audio_end(session: Session, payload: dict):
    final_text = session.last_asr_text
    session.last_asr_text = ""

    response = {"type": "asr:final", "payload": {"text": final_text}}
    await manager.send_personal_message(json.dumps(response), session.client_id)

    if final_text:
        await handle_user_text(session, {"text": final_text})

message_handlers = {
    "session:start": handle_session_start,
    "user:text": handle_user_text,
    "user:interrupt": handle_user_interrupt,
    "user:audio_chunk": handle_user_audio_chunk,
    "user:audio_end": handle_user_audio_end,
}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    session = session_manager.create_session(client_id)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")
            payload = message.get("payload")

            if handler := message_handlers.get(message_type):
                await handler(session, payload)
            else:
                logger.warning(f"Unknown message type: {message_type}")

    except WebSocketDisconnect:
        if session.active_llm_task:
            session.active_llm_task.cancel()
        manager.disconnect(client_id)
        session_manager.remove_session(client_id)
        logger.info(f"Client {client_id} disconnected.")
