import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ModelSelector from './ModelSelector';
import PromptInput from './PromptInput';
import ShaderCanvas from './ShaderCanvas';
import { generateImage, getWorkflows } from '../api';

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
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState('');

  useEffect(() => {
    console.log("ImageGenerator component mounted");
    fetchWorkflows();
  }, []);

  const fetchWorkflows = async () => {
    try {
      console.log("Fetching workflows...");
      const availableWorkflows = await getWorkflows();
      console.log("Fetched workflows:", availableWorkflows);
      setWorkflows(availableWorkflows);
      if (availableWorkflows.length > 0) {
        setSelectedWorkflow(availableWorkflows[0]);
      } else {
        console.log("No workflows available");
      }
    } catch (error) {
      console.error("Error fetching workflows:", error);
      setError('Failed to fetch workflows');
    }
  };

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
      }, selectedWorkflow);
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

      <div>
        <label htmlFor="workflow-select">Select Workflow: </label>
        <select
          id="workflow-select"
          value={selectedWorkflow}
          onChange={(e) => setSelectedWorkflow(e.target.value)}
        >
          {workflows.map((workflow) => (
            <option key={workflow} value={workflow}>{workflow}</option>
          ))}
        </select>
      </div>

      {isLoading && <p>Generating image...</p>}
      {error && <p className="error">{error}</p>}

      {generatedImage && (
        <div className="generated-image">
          {useShaderCanvas ? (
            <ShaderCanvas imageUrl={generatedImage} />
          ) : (
            <img src={generatedImage} alt="Generated" />
          )}
          {originalPrompt && <p><strong>Original Prompt:</strong> {originalPrompt}</p>}
          {improvedPrompt && <p><strong>Improved Prompt:</strong> {improvedPrompt}</p>}
        </div>
      )}

      <button onClick={() => setUseShaderCanvas(!useShaderCanvas)}>
        {useShaderCanvas ? 'Show Regular Image' : 'Show Shader Canvas'}
      </button>
    </div>
  );
}

export default ImageGenerator;