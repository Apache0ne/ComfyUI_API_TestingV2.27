# ComfyUI API Testing

This project is a Flask-based web application that interfaces with ComfyUI to generate images based on user prompts.

## Project Structure
ComfyUI_API_Testing/ ├── comfyui_flask_project/ │ ├── app/ │ │ ├── static/ │ │ ├── templates/ │ │ │ └── index.html │ │ ├── init.py │ │ └── routes.py │ ├── config.py │ ├── requirements.txt │ └── run.py └── README.md


## Setup

1. Clone the repository:
bash git clone https://github.com/Apache0ne/ComfyUI_API_Testing.git


2. Navigate to the project directory:
bash cd ComfyUI_API_Testing/comfyui_flask_project


3. Install the required dependencies:
bash pip install -r requirements.txt


4. Ensure ComfyUI is running and accessible at the URL specified in `config.py`.

5. Run the Flask application:
bash python run.py


## Usage

1. Open a web browser and navigate to `http://localhost:5000`.
2. Enter a prompt in the text area.
3. Click "Generate Image" to create an image based on your prompt.

## Configuration

Adjust the `COMFYUI_API_URL` in `config.py` if ComfyUI is running on a different port or host.

## Note

This project is a work in progress (WIP).
