# ComfyUI Image Generator with LLM Integration

This project combines a React frontend with a Flask backend to create an advanced image generation system using ComfyUI workflows and Language Model (LLM) integration for prompt improvement.

## Features

- LLM setup for prompt enhancement (Ollama, SambaNova, Groq, Cerebras)
- Model and LoRA selection
- Image generation using ComfyUI workflows
- Shader effects on generated images using p5.js

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+
- ComfyUI installation

## Installation

1. Clone the repository:
bash git clone https://github.com/yourusername/comfyui_react_project.git cd comfyui_react_project


2. Set up the backend:
bash cd backend python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate pip install -r requirements.txt


3. Set up the frontend:
bash cd ../frontend npm install


## Configuration

1. Backend configuration:
   - Edit `backend/app.py` to set your ComfyUI API endpoint and other settings.

2. Frontend configuration:
   - Update the API base URL in `frontend/src/api.js` if your backend runs on a different port.

## Running the Application

1. Start the backend:
bash cd backend python app.py


2. Start the frontend:
bash cd frontend npm start


3. Open your browser and navigate to `http://localhost:3000`.

## Usage Guide

1. LLM Setup:
   - On first run, you'll be prompted to choose an LLM (Ollama, SambaNova, Groq, or Cerebras).
   - Enter the required information (API key, model name, etc.).

2. Image Generation:
   - Select a category, model, and optional LoRA from the dropdowns.
   - Enter your prompt in the text input.
   - Click "Generate" to create the image.

3. View Results:
   - The generated image will be displayed along with the original and improved prompts.
   - Toggle between the regular image view and shader effects using the button provided.

## How It Works

1. Frontend (React):
   - `Setup.js`: Handles LLM configuration.
   - `ImageGenerator.js`: Main component for image generation interface.
   - `ModelSelector.js`: Manages model and LoRA selection.
   - `PromptInput.js`: Handles user prompt input.
   - `ShaderCanvas.js`: Applies p5.js shader effects to generated images.

2. Backend (Flask):
   - Processes API requests from the frontend.
   - Interacts with the chosen LLM to improve prompts.
   - Constructs and sends ComfyUI workflows for image generation.
   - Serves generated images and prompt information back to the frontend.

3. LLM Integration:
   - The chosen LLM (e.g., Ollama) receives the user's prompt.
   - It generates an improved version of the prompt.
   - The improved prompt is used in the ComfyUI workflow.

4. ComfyUI Workflow:
   - The backend constructs a workflow based on the selected model, LoRA, and improved prompt.
   - This workflow is sent to the ComfyUI API for image generation.

5. Shader Effects:
   - Generated images can be displayed with custom shader effects using p5.js.
   - Shaders are defined in `frontend/src/shaders/`.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
