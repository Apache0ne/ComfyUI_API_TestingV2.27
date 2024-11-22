# ComfyUI Image Generator with Ollama

This project is a web application that integrates ComfyUI for image generation with Ollama for prompt improvement. It allows users to select models and LoRAs, input prompts, and generate images based on improved prompts.

## Features

- Model and LoRA selection based on categories
- Prompt improvement using locally running Ollama with Llama model
- Image generation using ComfyUI
- Display of original and improved prompts alongside generated images

## Prerequisites

- Python 3.7+
- Flask
- Ollama running locally with Llama2 model
- ComfyUI API accessible

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/ComfyUI_API_Testing.git cd ComfyUI_API_Testing


2. Install the required packages:
pip install -r requirements.txt


3. Ensure Ollama is running locally with the Llama2 model.

4. Make sure ComfyUI is running and accessible.

## Configuration

1. Update the `config.py` file with your ComfyUI API URL:
python COMFYUI_API_URL = 'http://127.0.0.1:8188/api' # Adjust if needed


2. Prepare your model and LoRA lists:
   - Create `CKPmodels.txt` and `Lmodels.txt` files
   - Format them with categories in square brackets and models/LoRAs listed under each category

## Running the Application

1. Start the Flask application:
python run.py


2. Open a web browser and navigate to `http://127.0.0.1:5000`

## Usage

1. Select a category from the dropdown
2. Choose a model and optionally a LoRA
3. Enter your prompt in the text area
4. Click "Generate Image"
5. View the original prompt, improved prompt, and generated image

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
