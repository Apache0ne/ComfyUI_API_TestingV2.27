# ComfyUI Image Generator with LLM Integration(NEW BUILD)(FMD IS DEPRECATED FOR NOW)

A React-based frontend for ComfyUI with LLM-enhanced prompt generation and shader effects.

## Features

- ComfyUI workflow integration
- LLM prompt enhancement (Ollama, SambaNova, Groq, Cerebras)
- Model and LoRA selection
- Real-time shader effects using p5.js

## Setup

1. Clone the repo:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_TestingV2.27.git
   cd ComfyUI_API_TestingV2.27/comfyui_react_project
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   cd frontend && npm install
   cd ../backend && pip install -r requirements.txt
   \`\`\`

3. Start the backend:
   \`\`\`bash
   cd backend && python app.py
   \`\`\`

4. Start the frontend:
   \`\`\`bash
   cd frontend && npm start
   \`\`\`

5. Access the app at `http://localhost:3000`

## Configuration

- Update LLM settings in `backend/app.py`
- Modify ComfyUI workflows in `backend/app.py`
- Adjust shader effects in `frontend/src/p5setup/sketch.js`

## License

MIT License
