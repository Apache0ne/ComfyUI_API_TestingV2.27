# ComfyUI API Testing

A Flask-based web application that interfaces with ComfyUI's API to generate images based on user prompts. This project demonstrates the integration of ComfyUI's image generation capabilities into a web application.

## Features

- Web interface for submitting text prompts
- Integration with ComfyUI API for image generation
- Real-time image display upon generation
- Customizable ComfyUI workflow
- Error handling and user feedback

## Prerequisites

- Python 3.7+
- ComfyUI instance running and accessible

## Setup

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Apache0ne/ComfyUI_API_Testing.git
   cd ComfyUI_API_Testing
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   pip install -r comfyui_flask_project/requirements.txt
   \`\`\`

3. Configure ComfyUI API URL in `comfyui_flask_project/config.py`

4. Run the application:
   \`\`\`bash
   python comfyui_flask_project/run.py
   \`\`\`

5. Access the web interface at `http://localhost:5000`

## Usage

1. Enter a text prompt in the web interface
2. Click "Generate Image"
3. Wait for the image to be generated and displayed

## Project Structure

- `comfyui_flask_project/`: Main project directory
  - `app/`: Flask application
    - `static/`: Static files (CSS, JS)
    - `templates/`: HTML templates
    - `routes.py`: Flask routes and ComfyUI API interaction
  - `config.py`: Configuration settings
  - `run.py`: Application entry point
- `requirements.txt`: Python dependencies

## ComfyUI Workflow

The project uses a predefined ComfyUI workflow, which includes:
- KSampler
- CheckpointLoaderSimple
- EmptyLatentImage
- CLIPTextEncode
- VAEDecode
- SaveImage
- LoraLoader

The workflow can be customized in `app/routes.py`.

## Configuration

Update `comfyui_flask_project/config.py` to set:
- `SECRET_KEY`: Flask secret key
- `COMFYUI_API_URL`: URL of your ComfyUI API endpoint
- `UPLOAD_FOLDER`: Directory for uploaded files
- `MAX_CONTENT_LENGTH`: Maximum upload file size

## Contributing

This project is a work in progress. Contributions, suggestions, and feedback are welcome. Please feel free to submit a Pull Request or open an issue.

## License

[Specify your license here]

## Acknowledgements

- ComfyUI project
- Flask framework

Note: Ensure ComfyUI is running and accessible at the configured API URL before using this application.
