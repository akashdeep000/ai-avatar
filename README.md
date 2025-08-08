# Open LLM VTuber

This project is a full-stack application for an open-source, LLM-powered VTuber. It includes a Python backend for AI processing and a React frontend for the user interface, both managed within this single repository.

## Project Structure

- `/` (root): Contains the Python backend (FastAPI).
- `/frontend`: Contains the React frontend (Vite).

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and pnpm
- Docker (for containerized deployment)

### Backend Setup

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment:**

    - Create a `.env` file in the root directory. You can copy `.env.example` if one exists.
    - Fill in the required API keys and settings in the `.env` file (see Configuration section below).

4.  **Run the backend server:**
    ```bash
    python3 main.py
    ```
    The backend will be available at `http://localhost:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install dependencies:**

    ```bash
    pnpm install
    ```

3.  **Run the frontend development server:**
    ```bash
    pnpm run dev
    ```
    The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use).

## Integrating the AI Avatar into Your React App

You can easily integrate the AI Avatar into your own React application by copying the `frontend/src/components/AIAvatar` directory.

### 1. Copy the Directory

Copy the entire `frontend/src/components/AIAvatar` directory into your React project's `src/components` folder.

### 2. Install Dependencies

You will need to install the following dependencies in your project:

```bash
pnpm install @ricky0123/vad-react uuid
```

### 3. Wrap Your App with the Provider

In your main application component (e.g., `App.tsx`), wrap your components with the `AIAvatarProvider`.

```tsx
import { AIAvatarProvider } from "./components/AIAvatar";

function App() {
  return (
    <AIAvatarProvider backendUrl="localhost:8000">
      {/* Your other components go here */}
    </AIAvatarProvider>
  );
}
```

### 4. Use the Avatar Canvas and Hooks

Now you can use the `AIAvatarCanvas` to display the avatar and the `useAIAvatar` hook to interact with it.

```tsx
import { AIAvatarCanvas, useAIAvatar } from "./components/AIAvatar";
import { useEffect } from "react";

function MyComponent() {
  const {
    connectionStatus,
    messages,
    characters,
    fetchCharacters,
    selectCharacter,
    connect,
    sendText,
    startRecording,
    stopRecording,
  } = useAIAvatar();
  const [text, setText] = useState("");

  useEffect(() => {
    fetchCharacters();
  }, [fetchCharacters]);

  return (
    <div>
      <div style={{ height: "500px", width: "500px" }}>
        <AIAvatarCanvas />
      </div>

      <div>Connection Status: {connectionStatus}</div>

      <div>
        <select onChange={(e) => selectCharacter(e.target.value)}>
          <option>Select a character</option>
          {characters.map((char) => (
            <option key={char.id} value={char.id}>
              {char.name}
            </option>
          ))}
        </select>
        <button onClick={connect} disabled={connectionStatus === "CONNECTED"}>
          Connect
        </button>
      </div>

      <div>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.author}:</strong> {msg.text}
          </div>
        ))}
      </div>

      <div>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button onClick={() => sendText(text)}>Send</button>
        <button onMouseDown={startRecording} onMouseUp={stopRecording}>
          Hold to Speak
        </button>
      </div>
    </div>
  );
}
```

## Backend Architecture

The backend is a FastAPI application with the following key components:

- **`src/main.py`**: The main application entry point, which defines the FastAPI app, WebSocket endpoint, and lifespan manager for loading models.
- **`src/config.py`**: Manages application configuration using Pydantic, loading settings from an `.env` file.
- **`src/connection_manager.py`**: Handles WebSocket connections.
- **`src/session_manager.py`**: Manages user sessions and state.
- **`src/character_manager.py`**: Loads and manages character definitions from YAML files.
- **`src/asr/`, `src/llm/`, `src/tts/`**: Contain the interfaces and implementations for the different AI models.

## WebSocket API

The frontend and backend communicate over a WebSocket connection. All messages are in JSON format with a `type` and `payload`.

### Client-to-Server Messages

- **`session:start`**: Initializes a new session.
  - `payload`: `{"character_id": "string"}`
- **`user:text`**: Sends a text message from the user.
  - `payload`: `{"text": "string"}`
- **`user:interrupt`**: Notifies the server to interrupt the current LLM response.
  - `payload`: `{}`
- **`user:audio_chunk`**: Streams a chunk of audio data from the user's microphone.
  - `payload`: `{"data": "base64_string"}`
- **`user:audio_end`**: Signals the end of an audio stream.
  - `payload`: `{}`

### Server-to-Client Messages

- **`session:ready`**: Confirms that a session has been created.
  - `payload`: `{"session_id": "string", "character": "object", "live2d_model_info": "object"}`
- **`avatar:speak`**: Contains the text, audio, and animation data for the avatar to speak.
  - `payload`: `{"text": "string", "audio": "base64_string", "expressions": "array", "motions": "array"}`
- **`avatar:idle`**: Signals that the avatar should return to an idle state.
  - `payload`: `{}`
- **`asr:partial`**: Provides a partial transcription of the user's speech.
  - `payload`: `{"text": "string"}`
- **`asr:final`**: Provides the final transcription of the user's speech.
  - `payload`: `{"text": "string"}`

## Docker Deployment

This project includes a `docker-compose.yml` file for easy containerized deployment of the backend service.

### Prerequisites

- Docker
- Docker Compose

### Running with Docker Compose

1.  **Ensure your `.env` file is configured:** The Docker Compose setup uses the `.env` file in the root directory for configuration.

2.  **Build and run the service:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image and start the backend service. The service will be available at `http://localhost:8000`.

3.  **Running in detached mode:**
    To run the service in the background, use the `-d` flag:

    ```bash
    docker-compose up --build -d
    ```

4.  **Stopping the service:**
    ```bash
    docker-compose down
    ```

## Configuration

Application settings are managed via an `.env` file in the root directory.

### LLM Configuration

- `LLM_ENGINE`: The language model engine to use (e.g., `open_router`, `google_gemini`). Default: `open_router`.
- `LLM_MODEL`: The specific model to use. Default: `z-ai/glm-4.5-air:free`.
- `OPENROUTER_API_KEY`: Your API key for OpenRouter.
- `GEMINI_API_KEY`: Your API key for Google Gemini.

### App Configuration

These variables must be prefixed with `APP_`.

- `APP_ASR_ENGINE`: The ASR engine to use. Options: `sherpa_onnx_asr`, `faster_whisper_asr`. Default: `sherpa_onnx_asr`.
- `APP_ASR_DEVICE`: The device for Automatic Speech Recognition (`cpu` or `cuda`). Default: `cpu`.
- `APP_TTS_DEVICE`: The device for Text-to-Speech (`cpu` or `cuda`). Default: `cpu`.
- `APP_ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS. Default: `*`.
