# AI Avatar

This project is a real-time AI avatar that can listen, think, and respond to users. It is built with a Python backend using FastAPI and a React frontend. The avatar is powered by a combination of Automatic Speech Recognition (ASR), Large Language Models (LLM), and Text-to-Speech (TTS) technologies.

## Features

- **Real-time Interaction**: The AI avatar can listen and respond to users in real-time.
- **Live2D Integration**: The avatar is rendered using Live2D, which allows for expressive and dynamic animations.
- **Modular Architecture**: The application is designed with a modular architecture that allows for easy extension and customization.
- **Configurable ASR and TTS**: The ASR and TTS engines can be easily configured through environment variables.
- **Audio Processing**: The application includes a configurable audio processing pipeline that can be used to improve ASR accuracy.
- **React Component**: The frontend is built as a reusable React component that can be easily integrated into other applications.

## Architecture

The application is composed of a Python backend and a React frontend.

### Backend

The backend is built with FastAPI and is responsible for:

- **WebSocket Communication**: The backend uses WebSockets to communicate with the frontend in real-time.
- **ASR, LLM, and TTS Integration**: The backend integrates with ASR, LLM, and TTS engines to power the AI avatar.
- **Audio Processing**: The backend includes an audio processing pipeline that can be used to improve ASR accuracy.

### Frontend

The frontend is built with React and is responsible for:

- **Rendering the Avatar**: The frontend uses the Live2D SDK to render the AI avatar.
- **User Interaction**: The frontend captures audio from the user's microphone and sends it to the backend for processing.
- **Displaying Responses**: The frontend displays the AI avatar's responses and animations.

## Getting Started

To get started with the project, you will need to have Python and Node.js installed on your system.

### Backend Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ai-avatar.git
    cd ai-avatar
    ```
2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file**:
    ```bash
    cp .env.example .env
    ```
5.  **Run the backend**:
    ```bash
    python3 main.py
    ```

### Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install the dependencies**:
    ```bash
    npm install
    ```
3.  **Setup the environment variables**:
    ```bash
    cp .env.example .env
    ```
4.  **Run the frontend**:
    ```bash
    npm run dev
    ```

## Configuration

The application can be configured through environment variables. The available options are documented in the `.env.example` file.

### LLM Settings

- `LLM_ENGINE`: The LLM engine to use. Options: `open_router`, `google_gemini`.
- `LLM_MODEL`: The LLM model to use.
- `OPENROUTER_API_KEY`: Your OpenRouter API key.
- `GEMINI_API_KEY`: Your Google Gemini API key.

### ASR Settings

- `ASR_ENGINE`: The ASR engine to use. Options: `sherpa_onnx_asr`, `faster_whisper_asr`.
- `ASR_DEVICE`: The device to use for ASR inference. Options: `cpu`, `cuda`.
- `ASR_MODEL`: The ASR model to use.
- `ASR_COMPUTE_TYPE`: The compute type for ASR. Options: `int8`, `fp16`, `fp32`.
- `ASR_CPU_THREADS`: The number of CPU threads for ASR.

### Available ASR Models

| Model Name                  | `sherpa_onnx_asr` | `faster_whisper_asr` |
| --------------------------- | :---------------: | :------------------: |
| `sense-voice`               |        ✅         |          ❌          |
| `parakeet`                  |        ✅         |          ❌          |
| `whisper-tiny`              |        ✅         |          ✅          |
| `whisper-tiny.en`           |        ✅         |          ✅          |
| `whisper-base`              |        ✅         |          ✅          |
| `whisper-base.en`           |        ✅         |          ✅          |
| `whisper-small`             |        ✅         |          ✅          |
| `whisper-small.en`          |        ✅         |          ✅          |
| `whisper-medium`            |        ✅         |          ✅          |
| `whisper-medium.en`         |        ✅         |          ✅          |
| `whisper-large-v1`          |        ✅         |          ❌          |
| `whisper-large-v2`          |        ✅         |          ✅          |
| `whisper-large-v3`          |        ✅         |          ✅          |
| `whisper-distil-small.en`   |        ✅         |          ✅          |
| `whisper-distil-medium.en`  |        ✅         |          ✅          |
| `whisper-distil-large-v2`   |        ✅         |          ✅          |
| `whisper-distil-large-v3`   |        ❌         |          ✅          |
| `whisper-distil-large-v3.5` |        ❌         |          ✅          |
| `whisper-turbo`             |        ✅         |          ✅          |

### App Settings

- `APP_ALLOWED_ORIGINS`: The allowed origins for CORS.
- `APP_DEBUG_SAVE_AUDIO`: Save original and normalized audio for debugging.
- `APP_ENABLE_AUDIO_PROCESSING`: Enable audio processing.
- `APP_NOISE_REDUCTION`: Enable noise reduction.
- `APP_LOUDNESS_NORMALIZATION`: Enable loudness normalization.

## Characters

Characters are defined in `.yaml` files in the `characters` directory. Each character has a unique persona, Live2D model, and TTS engine.

### Creating a New Character

To create a new character, you will need to:

1.  **Add a Live2D Model**: Add the character's Live2D model to the `live2d-models` directory.
2.  **Create a YAML File**: Create a new `.yaml` file in the `characters` directory.
3.  **Configure the Character**: Configure the character's name, persona, Live2D model, and TTS engine in the YAML file.

### Character Configuration

The following options are available for configuring a character:

- `name`: The name of the character.
- `llm_persona`: The character's persona.
- `live2d_model_name`: The name of the character's Live2D model.
- `tts_engine`: The TTS engine to use for the character.
- `extra_data`: Extra data for the character, such as a greeting message. (not in use currently)

### Live2D Models

Live2D models are defined in the `model_dict.json` file. Each model has a unique name, description, and URL.

#### Adding a New Live2D Model

To add a new Live2D model, you will need to:

1.  **Add the Model Files**: Add the model's files to the `live2d-models` directory.
2.  **Update `model_dict.json`**: Add a new entry to the `model_dict.json` file with the model's name, description, and URL.

#### Model Configuration

The following options are available for configuring a Live2D model in `model_dict.json`:

- `name`: The name of the model.
- `description`: A description of the model.
- `url`: The URL of the model's `.model3.json` file.
- `kScale`: The scale of the model.
- `initialXshift`: The initial X shift of the model.
- `initialYshift`: The initial Y shift of the model.
- `kXOffset`: The X offset of the model.
- `idleMotionGroupName`: The name of the idle motion group.
- `emotionMap`: A map of emotions to expression files.
- `motionMap`: A map of motions to motion files.
- `tapMotions`: A map of tap motions to motion files.

## Integration Guide

The AI Avatar can be easily integrated into any React application.

> For more advanced usage examples, please refer to the files in the `frontend/src/examples` directory.

### 1. Copy the `AIAvatar` Component

Copy the `frontend/src/components/AIAvatar` directory to your React application's `src/components` directory.

### 2. Install the Dependencies

Install the following dependencies in your React application:

```bash
npm install @ricky0123/vad-react
```

### 3. Use the `AIAvatarProvider` and `AIAvatarCanvas`

Wrap your application with the `AIAvatarProvider` and use the `AIAvatarCanvas` to render the avatar.

```tsx
import React from "react";
import { AIAvatarProvider, AIAvatarCanvas } from "./components/AIAvatar";

function App() {
  return (
    <AIAvatarProvider backendUrl="http://localhost:8000">
      <AIAvatarCanvas />
    </AIAvatarProvider>
  );
}

export default App;
```

### 4. Use the `useAIAvatar` Hook

Use the `useAIAvatar` hook to interact with the AI avatar.

```tsx
import React from "react";
import { useAIAvatar } from "./components/AIAvatar";

function MyComponent() {
  const {
    sendText,
    startRecording,
    stopRecording,
    connect,
    fetchCharacters,
    selectCharacter,
    characters,
  } = useAIAvatar();

  React.useEffect(() => {
    connect();
    fetchCharacters();
  }, [connect, fetchCharacters]);

  React.useEffect(() => {
    if (characters.length > 0) {
      selectCharacter(characters[0].id);
    }
  }, [characters, selectCharacter]);

  return (
    <div>
      <button onClick={() => sendText("Hello, world!")}>Send Text</button>
      <button onClick={startRecording}>Start Recording</button>
      <button onClick={stopRecording}>Stop Recording</button>
    </div>
  );
}
```
