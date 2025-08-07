import React from 'react';
import { Live2DCanvas } from './Live2DCanvas';
import { useAIAvatar } from './useAIAvatar';

export const AIAvatarCanvas: React.FC = () => {
    const { isCharecterLoaded, connectionStatus } = useAIAvatar();

    if (connectionStatus !== 'CONNECTED' || !isCharecterLoaded) {

        return <div className="flex items-center justify-center h-full">Loading Character...</div>;
    }

    return <Live2DCanvas />;
};