import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import PromptInput from './PromptInput';
import SideMenu from './SideMenu';
import MainContent from './MainContent';
import { generateImage } from '../api/api';
import '../styles/ImageGenerator.css';

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
  const [savedPrompts, setSavedPrompts] = useState([]);
  const [isSaveEnabled, setIsSaveEnabled] = useState(true); // Default to save enabled
  const [feedback, setFeedback] = useState('');
  const [isSideMenuOpen, setIsSideMenuOpen] = useState(false); // State to track side menu open/close

  const promptDisplayRef = useRef(null);

  const handleModelSelect = ({ category, model, lora }) => {
    setSelectedCategory(category);
    setSelectedModel(model);
    setSelectedLora(lora);
    // Do not close the side menu after selection
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

      if (isSaveEnabled) {
        const prompts = {
          original: result.original_prompt,
          improved: result.improved_prompt
        };
        setSavedPrompts([...savedPrompts, prompts]);
        localStorage.setItem('savedPrompts', JSON.stringify([...savedPrompts, prompts]));
        setFeedback('Prompts saved successfully.');
        setTimeout(() => setFeedback(''), 3000); // Clear feedback after 3 seconds
      }
    } catch (error) {
      setError('Failed to generate image');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleSave = () => {
    const newSaveEnabled = !isSaveEnabled;
    setIsSaveEnabled(newSaveEnabled);
    localStorage.setItem('isSaveEnabled', newSaveEnabled); // Persist the toggle state
    setFeedback(newSaveEnabled ? 'Prompt saving enabled.' : 'Prompt saving disabled.');
    setTimeout(() => setFeedback(''), 3000); // Clear feedback after 3 seconds
  };

  const toggleSideMenu = () => {
    setIsSideMenuOpen(!isSideMenuOpen);
  };

  useEffect(() => {
    const storedPrompts = JSON.parse(localStorage.getItem('savedPrompts')) || [];
    setSavedPrompts(storedPrompts);

    const storedSaveEnabled = JSON.parse(localStorage.getItem('isSaveEnabled')) !== false; // Default to true if not set
    setIsSaveEnabled(storedSaveEnabled);
  }, []);

  useEffect(() => {
    if (promptDisplayRef.current) {
      promptDisplayRef.current.scrollTop = promptDisplayRef.current.scrollHeight;
    }
  }, [originalPrompt, improvedPrompt, savedPrompts]);

  return (
    <div className="image-generator-container">
      <button onClick={() => navigate(-1)}>Back</button>
      <h2>Generate Image</h2>
      <div className="image-generator">
        <SideMenu
          isSideMenuOpen={isSideMenuOpen}
          toggleSideMenu={toggleSideMenu}
          onModelSelect={handleModelSelect}
        />
        <MainContent
          isLoading={isLoading}
          error={error}
          feedback={feedback}
          generatedImage={generatedImage}
          useShaderCanvas={useShaderCanvas}
          setUseShaderCanvas={setUseShaderCanvas}
          originalPrompt={originalPrompt}
          improvedPrompt={improvedPrompt}
          savedPrompts={savedPrompts}
        />
        <div className="chat-box">
          <div className="prompt-display" ref={promptDisplayRef}>
            {savedPrompts.map((prompts, index) => (
              <div key={index} className="prompt-message">
                <p className="user-prompt">
                  <strong>Original Prompt:</strong> {prompts.original}
                </p>
                <p className="improved-prompt">
                  <strong>Improved Prompt:</strong> {prompts.improved}
                </p>
              </div>
            ))}
            {originalPrompt && (
              <div className="prompt-message">
                <p className="user-prompt">
                  <strong>Your Prompt:</strong> {originalPrompt}
                </p>
              </div>
            )}
            {improvedPrompt && (
              <div className="prompt-message">
                <p className="improved-prompt">
                  <strong>Improved Prompt:</strong> {improvedPrompt}
                </p>
              </div>
            )}
          </div>
          <div className="prompt-input">
            <PromptInput onSubmit={handlePromptSubmit} />
            <div className="toggle-save">
              <label className="switch">
                <input
                  type="checkbox"
                  checked={isSaveEnabled}
                  onChange={handleToggleSave}
                />
                <span className="slider round"></span>
              </label>
              <span>Save Prompts</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImageGenerator;