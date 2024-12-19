# ComfyUI Image Generator with LLM Integration
## all Future work on this project is private 
This project combines ComfyUI for image generation with various Language Model (LLM) providers, offering a web-based interface for creating and manipulating images.

## Features

- Image generation using ComfyUI
- LLM integration (Ollama, SambaNova, Groq, Cerebras)
- Shader effects with p5.js
- React frontend
- Flask backend

## Prerequisites

- Python 3.8+
- Node.js and npm
- ComfyUI setup (not included)

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_TestingV3.3.git
   cd ComfyUI_API_TestingV3.3/ADTEST
   \`\`\`

2. Set up the backend:
   \`\`\`bash
   cd backend
   pip install -r requirements.txt
   \`\`\`

3. Set up the frontend:
   \`\`\`bash
   cd ../frontend
   npm install
   \`\`\`

## Configuration

1. Backend: Adjust `CKPmodels.txt` and `Lmodels.txt` for available models.
2. Frontend: Configure API endpoints in `src/api/api.js` if necessary.

## Running the Application

1. Start the backend:
   \`\`\`bash
   cd backend
   python app.py
   \`\`\`

2. Start the frontend:
   \`\`\`bash
   cd frontend
   npm start
   \`\`\`

3. Access the application at `http://localhost:3000`

## Usage

1. Set up your preferred LLM provider in the Setup page.
2. Use the Image Generator to create and manipulate images.
3. Apply shader effects using the p5.js integration.

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests with your changes.

## License

[MIT License](LICENSE)
