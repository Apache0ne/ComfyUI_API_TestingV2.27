import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ModelSelector from './ModelSelector';
import PromptInput from './PromptInput';
import { generateImage } from '../api';

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

  return (
    <div className="image-generator">
      <button onClick={() => navigate(-1)}>Back</button>
      <h2>Generate Image</h2>
      <ModelSelector onModelSelect={handleModelSelect} />
      <PromptInput onSubmit={handlePromptSubmit} />

      {isLoading && <p>Generating image...</p>}
      {error && <p className="error">{error}</p>}

      {generatedImage && (
        <div className="generated-image">
          <img src={generatedImage} alt="Generated" />
          <p><strong>Original Prompt:</strong> {originalPrompt}</p>
          <p><strong>Improved Prompt:</strong> {improvedPrompt}</p>
        </div>
      )}
    </div>
  );
}

export default ImageGenerator;
