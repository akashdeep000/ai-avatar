import { useAIAvatar } from '@/hooks/useAIAvatar';
import { createContext } from 'react';

type AIAvatarContextType = ReturnType<typeof useAIAvatar>;

export const AIAvatarContext = createContext<AIAvatarContextType | undefined>(undefined);