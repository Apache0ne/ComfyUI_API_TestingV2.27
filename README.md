# ComfyUI Image Generator with LLM Integration

This project is a web application that integrates ComfyUI for image generation with various Language Model (LLM) options for prompt improvement. It allows users to configure their LLM choice, select models and LoRAs, input prompts, and generate images based on improved prompts.

## Features

- Initial setup page for LLM configuration (Ollama, SambaNova, Groq, Cerebras)
- Model and LoRA selection based on categories
- Prompt improvement using selected LLM
- Image generation using ComfyUI
- Display of original and improved prompts alongside generated images

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm 6+
- ComfyUI API accessible
- Chosen LLM (e.g., Ollama running locally, or API access to other LLMs)

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/comfyui-react-project.git cd comfyui-react-project


2. Set up the backend:
cd backend pip install -r requirements.txt


3. Set up the frontend:
cd ../frontend npm install


4. Configure the ComfyUI API URL in `backend/config.py`:
python COMFYUI_API_URL = 'http://127.0.0.1:8188/api' # Adjust if needed


5. Prepare your model and LoRA lists:
   - Edit `backend/CKPmodels.txt` and `backend/Lmodels.txt`
   - Format them with categories in square brackets and models/LoRAs listed under each category

## Running the Application

1. Start the backend:
cd backend python app.py


2. In a new terminal, start the frontend:
cd frontend npm start


3. Open a web browser and navigate to `http://localhost:3000`

## Usage

1. On first run, complete the setup page to configure your LLM choice
2. On the main page, select a category from the dropdown
3. Choose a model and optionally a LoRA
4. Enter your prompt in the text area
5. Click "Generate Image"
6. View the original prompt, improved prompt, and generated image

## Project Structure

- `backend/`: Flask backend
  - `app.py`: Main Flask application
  - `config.py`: Configuration settings
  - `requirements.txt`: Python dependencies
- `frontend/`: React frontend
  - `src/`: Source files
    - `components/`: React components
    - `App.js`: Main React component
    - `api.js`: API interaction functions
  - `package.json`: Node.js dependencies and scripts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.