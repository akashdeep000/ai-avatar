import { useEffect } from 'react';
import { AIAvatarProvider, useAIAvatar } from './components/AIAvatar';
import CharacterSelection from './components/CharacterSelection';
import MainView from './examples/MainView';

function AppContent() {
  const { characters, character, selectCharacter, fetchCharacters } = useAIAvatar();

  useEffect(() => {
    fetchCharacters();
  }, [fetchCharacters]);

  if (!character) {
    return <CharacterSelection characters={characters} onCharacterSelected={(char) => selectCharacter(char.id)} />;
  }

  return <MainView />;
}

function App() {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  if (!backendUrl) {
    return (
      <div className="flex h-screen w-screen items-center justify-center">
        <p className="text-red-500">
          VITE_BACKEND_URL is not set. Please check your .env file.
        </p>
      </div>
    );
  }

  return (
    <AIAvatarProvider backendUrl={backendUrl}>
      <div className="h-svh">
        <AppContent />
      </div>
    </AIAvatarProvider>
  );
}

export default App;

