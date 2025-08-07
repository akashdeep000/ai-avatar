import { useAIAvatar } from '@/hooks/useAIAvatar';
import { AIAvatarContext } from './ai-avatar-context';

export const AIAvatarProvider = ({ children }: { children: React.ReactNode }) => {
    const aiAvatar = useAIAvatar();

    return (
        <AIAvatarContext.Provider value={aiAvatar}>
            {children}
        </AIAvatarContext.Provider>
    );
};