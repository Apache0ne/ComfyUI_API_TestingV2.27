import React, { useState, useEffect } from 'react';
import Setup from './components/Setup';
import ImageGenerator from './components/ImageGenerator';
import { getLLMSetup } from './api';
import './App.css';

function App() {
  const [isSetupComplete, setIsSetupComplete] = useState(false);

  useEffect(() => {
    checkSetup();
  }, []);

  const checkSetup = async () => {
    try {
      const setup = await getLLMSetup();
      setIsSetupComplete(setup.isComplete);
    } catch (error) {
      console.error('Failed to check setup:', error);
    }
  };

  const handleSetupComplete = () => {
    setIsSetupComplete(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ComfyUI Image Generator</h1>
      </header>
      <main>
        {!isSetupComplete ? (
          <Setup onSetupComplete={handleSetupComplete} />
        ) : (
          <ImageGenerator />
        )}
      </main>
    </div>
  );
}

export default App;