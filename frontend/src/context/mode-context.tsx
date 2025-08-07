import { createContext } from 'react';

export type Mode = 'pet' | 'normal';

interface ModeContextType {
    mode: Mode;
    setMode: (mode: Mode) => void;
}

export const ModeContext = createContext<ModeContextType | undefined>(undefined);