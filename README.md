# ComfyUI API Testing with Ollama Integration

A Flask-based web interface for generating images using ComfyUI's API, enhanced with Ollama-powered prompt refinement.

## Features
- Web UI for prompt input
- Ollama integration for prompt refinement
- Display of original and refined prompts
- ComfyUI API integration for image generation
- Asynchronous image processing and display

## Requirements
- Python 3.7+
- Flask
- Requests
- Pillow
- Ollama

## Setup
1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_Testing.git
   cd ComfyUI_API_Testing
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Ensure ComfyUI is running locally (default: http://127.0.0.1:8188)

4. Install and run Ollama with the required model (e.g., llama2)

## Usage
1. Run the Flask app:
   \`\`\`bash
   python run.py
   \`\`\`

2. Access the web interface at `http://localhost:5000`

3. Enter a prompt, submit, and view the original prompt, refined prompt, and generated image

## Configuration
Adjust ComfyUI API URL, Ollama settings, and other configurations in `config.py`

## Note
This project is under active development. Contributions and feedback are welcome.