# ComfyUI API Testing V2.28.2

A React-based frontend and Flask-based backend for ComfyUI Image Generator with LLM integration.

## Features

- Image generation using ComfyUI workflows
- Model and LoRA selection
- Prompt input with LLM-based improvement
- Workflow customization
- 3D image visualization using P5.js and WebGL shaders

## Prerequisites

- Node.js (v14.0.0 or later)
- Python (v3.8 or later)
- ComfyUI installation

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_TestingV2.28.2.git
   cd ComfyUI_API_TestingV2.28.2
   \`\`\`

2. Set up the frontend:
   \`\`\`bash
   cd comfyui_react_project/frontend
   npm install
   \`\`\`

3. Set up the backend:
   \`\`\`bash
   cd ../backend
   pip install -r requirements.txt
   \`\`\`

## Usage

1. Start the backend:
   \`\`\`bash
   cd comfyui_react_project/backend
   python app.py
   \`\`\`

2. Start the frontend:
   \`\`\`bash
   cd ../frontend
   npm start
   \`\`\`

3. Open http://localhost:3000 in your browser.

## Configuration

- Backend port: 5000 (default)
- Frontend port: 3000 (default)
- Adjust API endpoints in `frontend/src/api.js` if needed

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
