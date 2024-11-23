# ComfyUI API Testing V3 React

A React-based frontend for ComfyUI image generation with LLM integration.

## Features

- Image generation using ComfyUI
- LLM integration for prompt improvement
- Model and LoRA selection
- Support for multiple LLM providers (Ollama, SambaNova, Groq, Cerebras)

## Structure

- `frontend/`: React application
- `backend/`: Flask API server

## Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_TestingV3_react.git
   cd ComfyUI_API_TestingV3_react
   \`\`\`

2. Set up the backend:
   \`\`\`bash
   cd comfyui_react_project/backend
   pip install -r requirements.txt
   \`\`\`

3. Set up the frontend:
   \`\`\`bash
   cd ../frontend
   npm install
   \`\`\`

## Running

1. Start the backend:
   \`\`\`bash
   cd comfyui_react_project/backend
   python app.py
   \`\`\`

2. Start the frontend:
   \`\`\`bash
   cd comfyui_react_project/frontend
   npm start
   \`\`\`

3. Access the application at `http://localhost:3000`

## Configuration

- Backend: Edit `config.py` for API URLs and model paths
- Frontend: Update API endpoint in `src/api.js` if needed

## Contributing

Please read CONTRIBUTING.md for details on code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
