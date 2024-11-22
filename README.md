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
- Flask
- ComfyUI API accessible
- Chosen LLM (e.g., Ollama running locally, or API access to other LLMs)

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/ComfyUI_API_TestingV1.git
   cd ComfyUI_API_TestingV1/comfyui_flask_project
   \`\`\`

2. Install the required packages:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Ensure your chosen LLM is set up and accessible.

4. Make sure ComfyUI is running and accessible.

## Configuration

1. Update the `config.py` file with your ComfyUI API URL:
   \`\`\`python
   COMFYUI_API_URL = 'http://127.0.0.1:8188/api' # Adjust if needed
   \`\`\`

2. Prepare your model and LoRA lists:
   - Create `CKPmodels.txt` and `Lmodels.txt` files
   - Format them with categories in square brackets and models/LoRAs listed under each category

## Running the Application

1. Start the Flask application:
   \`\`\`bash
   python run.py
   \`\`\`

2. Open a web browser and navigate to `http://127.0.0.1:5000`

## Usage

1. On first run, complete the setup page to configure your LLM choice
2. On the main page, select a category from the dropdown
3. Choose a model and optionally a LoRA
4. Enter your prompt in the text area
5. Click "Generate Image"
6. View the original prompt, improved prompt, and generated image

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
