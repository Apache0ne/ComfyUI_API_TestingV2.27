import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ModelSelector from './ModelSelector';
import PromptInput from './PromptInput';
import ShaderCanvas from './ShaderCanvas';
import { generateImage } from '../api/api';

function ImageGenerator() {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedLora, setSelectedLora] = useState('');
  const [generatedImage, setGeneratedImage] = useState(null);
  const [originalPrompt, setOriginalPrompt] = useState('');
  const [improvedPrompt, setImprovedPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [useShaderCanvas, setUseShaderCanvas] = useState(false);
  const promptDisplayRef = useRef(null);

  const handleModelSelect = ({ category, model, lora }) => {
    setSelectedCategory(category);
    setSelectedModel(model);
    setSelectedLora(lora);
  };

  const handlePromptSubmit = async (promptText) => {
    setIsLoading(true);
    setError('');
    setGeneratedImage(null);
    setOriginalPrompt('');
    setImprovedPrompt('');

    try {
      const result = await generateImage({
        category: selectedCategory,
        model: selectedModel,
        lora: selectedLora,
        prompt: promptText
      });
      setGeneratedImage(result.image_url);
      setOriginalPrompt(result.original_prompt);
      setImprovedPrompt(result.improved_prompt);
    } catch (error) {
      setError('Failed to generate image');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (promptDisplayRef.current) {
      promptDisplayRef.current.scrollTop = promptDisplayRef.current.scrollHeight;
    }
  }, [originalPrompt, improvedPrompt]);

  return (
    <div className="image-generator-container">
      <button onClick={() => navigate(-1)}>Back</button>
      <h2>Generate Image</h2>
      <div className="image-generator">
        <div className="side-menu">
          <ModelSelector onModelSelect={handleModelSelect} />
          <PromptInput onSubmit={handlePromptSubmit} />
        </div>
        <div className="main-content">
          {isLoading && <p>Generating image...</p>}
          {error && <p className="error">{error}</p>}

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
        <div className="prompt-display" ref={promptDisplayRef}>
          {originalPrompt && (
            <p className="prompt-message original-prompt">
              <strong>Original Prompt:</strong> {originalPrompt}
            </p>
          )}
          {improvedPrompt && (
            <p className="prompt-message improved-prompt">
              <strong>Improved Prompt:</strong> {improvedPrompt}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ImageGenerator;