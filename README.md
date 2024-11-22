# ComfyUI API Testing with Ollama Integration

A Flask-based web interface for generating images using ComfyUI's API, enhanced with Ollama-powered prompt refinement and categorized checkpoint model selection.

## Features
- Web UI for prompt input and model selection
- Categorized checkpoint models (SDXL, SD, FLUX)
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

5. Create and populate `CKPmodels.txt` with your checkpoint model filenames, categorized under SDXL, SD, and FLUX

## Usage
1. Run the Flask app:
   \`\`\`bash
   python run.py
   \`\`\`

2. Access the web interface at `http://localhost:5000`

3. Select a model category and specific model
4. Enter a prompt and submit
5. View the original prompt, refined prompt, and generated image

## Configuration
- Adjust ComfyUI API URL and other settings in `config.py`
- Manage available checkpoint models by editing `CKPmodels.txt`

## Customizing Checkpoint Models
To add or remove checkpoint models:
1. Open `CKPmodels.txt`
2. Add or remove model filenames under the appropriate category ([SDXL], [SD], or [FLUX])
3. Save the file and restart the Flask app

Example `CKPmodels.txt`:
[SDXL]\
creapromptLightning_creapromtHypersdxlV1.safetensors\
sdxl_model2.safetensors\

[SD]\
epicrealism_naturalSinRC1VAE.safetensors\
sd_model2.safetensors\

[FLUX]\
flux1-dev-bnb-nf4-v2.safetensors\
flux_model2.safetensors

## Note
This project is under active development. Contributions and feedback are welcome.
