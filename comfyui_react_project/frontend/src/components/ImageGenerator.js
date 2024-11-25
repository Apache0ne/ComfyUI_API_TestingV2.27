import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ModelSelector from './ModelSelector';
import PromptInput from './PromptInput';
import ShaderCanvas from './ShaderCanvas';
import { generateImage, getWorkflows } from '../api';

function ImageGenerator() {
  const navigate = useNavigate();
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
  
  // State variables for additional parameters
  const [seed, setSeed] = useState(1113884446105075);
  const [steps, setSteps] = useState(4);
  const [cfg, setCfg] = useState(1);
  const [samplerName, setSamplerName] = useState("dpmpp_sde");
  const [scheduler, setScheduler] = useState("normal");
  const [denoise, setDenoise] = useState(1);
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(1024);
  const [batchSize, setBatchSize] = useState(1);
  const [loraStrengthModel, setLoraStrengthModel] = useState(1);
  const [loraStrengthClip, setLoraStrengthClip] = useState(1);

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

  const handleModelSelect = ({ model, lora }) => {
    setSelectedModel(model);
    setSelectedLora(lora);
  };

  const handlePromptSubmit = async (promptText) => {
    setIsLoading(true);
    setError('');
    setGeneratedImage(null);
    setOriginalPrompt('');
    setImprovedPrompt('');

    const imageData = {
      prompt: promptText,
      selected_model: selectedModel,
      lora: selectedLora,
      seed,
      steps,
      cfg,
      sampler_name: samplerName,
      scheduler,
      denoise,
      width,
      height,
      batch_size: batchSize,
      lora_strength_model: loraStrengthModel,
      lora_strength_clip: loraStrengthClip
    };

    console.log("Sending data to backend:", { workflow: selectedWorkflow, inputs: imageData });

    try {
      const result = await generateImage(imageData, selectedWorkflow);
      console.log("Received result:", result);
      setGeneratedImage(result.image_url);
      setOriginalPrompt(result.original_prompt);
      setImprovedPrompt(result.improved_prompt);
    } catch (error) {
      console.error("Error generating image:", error);
      setError('Failed to generate image: ' + error.message);
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

      <div>
        <label htmlFor="seed">Seed: </label>
        <input 
          type="number" 
          id="seed" 
          value={seed} 
          onChange={(e) => setSeed(Number(e.target.value))} 
        />
      </div>
      <div>
        <label htmlFor="steps">Steps: </label>
        <input 
          type="number" 
          id="steps" 
          value={steps} 
          onChange={(e) => setSteps(Number(e.target.value))} 
        />
      </div>
      <div>
        <label htmlFor="cfg">CFG Scale: </label>
        <input 
          type="number" 
          id="cfg" 
          value={cfg} 
          onChange={(e) => setCfg(Number(e.target.value))} 
          step="0.1" 
        />
      </div>
      <div>
        <label htmlFor="sampler">Sampler: </label>
        <select 
          id="sampler" 
          value={samplerName} 
          onChange={(e) => setSamplerName(e.target.value)}
        >
          <option value="dpmpp_sde">DPM++ SDE</option>
          <option value="euler_a">Euler Ancestral</option>
          {/* Add more sampler options as needed */}
        </select>
      </div>
      <div>
        <label htmlFor="scheduler">Scheduler: </label>
        <select 
          id="scheduler" 
          value={scheduler} 
          onChange={(e) => setScheduler(e.target.value)}
        >
          <option value="normal">Normal</option>
          <option value="karras">Karras</option>
          {/* Add more scheduler options as needed */}
        </select>
      </div>
      <div>
        <label htmlFor="denoise">Denoise: </label>
        <input 
          type="number" 
          id="denoise" 
          value={denoise} 
          onChange={(e) => setDenoise(Number(e.target.value))} 
          step="0.01" 
          min="0" 
          max="1" 
        />
      </div>
      <div>
        <label htmlFor="width">Width: </label>
        <input 
          type="number" 
          id="width" 
          value={width} 
          onChange={(e) => setWidth(Number(e.target.value))} 
          step="8" 
        />
      </div>
      <div>
        <label htmlFor="height">Height: </label>
        <input 
          type="number" 
          id="height" 
          value={height} 
          onChange={(e) => setHeight(Number(e.target.value))} 
          step="8" 
        />
      </div>
      <div>
        <label htmlFor="batchSize">Batch Size: </label>
        <input 
          type="number" 
          id="batchSize" 
          value={batchSize} 
          onChange={(e) => setBatchSize(Number(e.target.value))} 
          min="1" 
        />
      </div>
      <div>
        <label htmlFor="loraStrengthModel">LoRA Strength (Model): </label>
        <input 
          type="number" 
          id="loraStrengthModel" 
          value={loraStrengthModel} 
          onChange={(e) => setLoraStrengthModel(Number(e.target.value))} 
          step="0.01" 
        />
      </div>
      <div>
        <label htmlFor="loraStrengthClip">LoRA Strength (CLIP): </label>
        <input 
          type="number" 
          id="loraStrengthClip" 
          value={loraStrengthClip} 
          onChange={(e) => setLoraStrengthClip(Number(e.target.value))} 
          step="0.01" 
        />
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