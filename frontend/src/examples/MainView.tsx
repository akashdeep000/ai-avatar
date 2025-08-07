import React, { useEffect } from 'react';
import { AIAvatarCanvas, useAIAvatar } from '../components/AIAvatar';
import Chat from './Chat';

const MainView: React.FC = () => {
    const {
        messages,
        voiceInput,
        partialTranscript,
        aiState,
        asrState,
        sendText,
        startRecording,
        stopRecording,
        interrupt,
        setVoiceInput,
        connect,
    } = useAIAvatar();

    useEffect(() => {
        connect();
    }, [connect]);

    const setRecordingMode = (mode: 'conversation' | 'manual') => {
        if (mode === 'manual') {
            setVoiceInput({ mode: 'manual' });
        } else {
            setVoiceInput({ mode: 'conversation', continuous: voiceInput.mode === 'conversation' ? voiceInput.continuous : false });
        }
    };

    const setContinuousListening = (enabled: boolean) => {
        if (voiceInput.mode === 'conversation') {
            setVoiceInput({ ...voiceInput, continuous: enabled });
        }
    };

    return (
        <div className="flex h-full">
            <div className="w-2/3 h-full">
                <AIAvatarCanvas />
            </div>
            <div className="w-1/3 h-full border-l">
                <Chat
                    onSendMessage={sendText}
                    messages={messages}
                    aiState={aiState}
                    asrState={asrState}
                    voiceInput={voiceInput}
                    partialTranscript={partialTranscript}
                    recordingMode={voiceInput.mode}
                    setRecordingMode={setRecordingMode}
                    continuousListening={voiceInput.mode === 'conversation' ? voiceInput.continuous : false}
                    setContinuousListening={setContinuousListening}
                    startRecording={startRecording}
                    stopRecording={stopRecording}
                    interrupt={interrupt}
                />
            </div>
        </div>
    );
};

export default MainView;