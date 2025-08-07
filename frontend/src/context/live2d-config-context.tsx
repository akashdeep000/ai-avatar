import { createContext } from 'react';

export interface ModelInfo {
    url: string;
    kScale?: number;
    initialXshift?: number;
    initialYshift?: number;
    pointerInteractive?: boolean;
    defaultEmotion?: string | number;
    tapMotions?: Record<string, unknown>;
    scrollToResize?: boolean;
}

export interface Character {
    id: string;
    name: string;
    live2d_model_info: ModelInfo;
}

interface Live2DConfigContextType {
    character?: Character;
    setCharacter: (character: Character) => void;
}

export const Live2DConfigContext = createContext<Live2DConfigContextType | undefined>(undefined);