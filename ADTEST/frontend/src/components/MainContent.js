import React, { useRef } from 'react';
import ShaderCanvas from './ShaderCanvas';
import '../styles/MainContent.css';

const MainContent = ({
  isLoading,
  error,
  feedback,
  generatedImage,
  useShaderCanvas,
  setUseShaderCanvas,
  originalPrompt,
  improvedPrompt,
  savedPrompts,
}) => {
  const promptDisplayRef = useRef(null);

  React.useEffect(() => {
    if (promptDisplayRef.current) {
      promptDisplayRef.current.scrollTop = promptDisplayRef.current.scrollHeight;
    }
  }, [originalPrompt, improvedPrompt, savedPrompts]);

  return (
    <div className="main-content">
      {isLoading && <p>Generating image...</p>}
      {error && <p className="error">{error}</p>}
      {feedback && <p className="feedback">{feedback}</p>}

      {generatedImage && (
        <div className="generated-image">
          {useShaderCanvas ? (
            <ShaderCanvas imageUrl={generatedImage} />
          ) : (
            <img src={generatedImage} alt="Generated" />
          )}
        </div>
      )}
      <button onClick={() => setUseShaderCanvas(!useShaderCanvas)}>
        {useShaderCanvas ? 'Show Regular Image' : 'Show Shader Canvas'}
      </button>
    </div>
  );
};

export default MainContent;