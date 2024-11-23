const API_BASE_URL = 'http://localhost:5000/api';

export const getCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/categories`);
  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }
  return response.json();
};

export const getModelsAndLoras = async (category) => {
  const response = await fetch(`${API_BASE_URL}/models?category=${encodeURIComponent(category)}`);
  if (!response.ok) {
    throw new Error('Failed to fetch models and LoRAs');
  }
  return response.json();
};

export const generateImage = async (promptData) => {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(promptData),
  });
  if (!response.ok) {
    throw new Error('Failed to generate image');
  }
  return response.json();
};

export const saveLLMSetup = async (setupData) => {
  const response = await fetch(`${API_BASE_URL}/setup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(setupData),
  });
  if (!response.ok) {
    const errorText = await response.text(); // Add this line
    throw new Error(`Failed to save LLM setup: ${errorText}`); // Modify this line
  }
  return response.json();
};

export const getLLMSetup = async () => {
  const response = await fetch(`${API_BASE_URL}/setup`);
  if (!response.ok) {
    throw new Error('Failed to fetch LLM setup');
  }
  return response.json();
};
