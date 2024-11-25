from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from config import Config
import requests
from services.comfyui_service import ComfyUIService
from services.llm_service import LLMService
from utils.http_client import HTTPClient
from utils.html_utils import escape_html

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)

comfyui_service = ComfyUIService(app.config['COMFYUI_API_URL'])
llm_service = LLMService(app.config['LLM_CONFIG'])
http_client = HTTPClient()

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(list(app.config['CHECKPOINT_MODELS'].keys()))

@app.route('/api/models', methods=['GET'])
def get_models_and_loras():
    category = request.args.get('category')
    return jsonify({
        'models': app.config['CHECKPOINT_MODELS'].get(category, []),
        'loras': app.config['LORA_MODELS'].get(category, [])
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    original_prompt = data['prompt']
    category = data['category']
    selected_model = data['model']
    selected_lora = data.get('lora', '')

    improved_prompt = llm_service.improve_prompt(original_prompt)

    workflow = comfyui_service.create_workflow(selected_model, selected_lora, improved_prompt)

    try:
        response = http_client.post(app.config['COMFYUI_API_URL'] + "/prompt", json={"prompt": workflow})
        if response.status_code == 200:
            prompt_id = response.json()['prompt_id']
            
            while True:
                try:
                    history_response = http_client.get(f"{app.config['COMFYUI_API_URL']}/history/{prompt_id}")
                    if history_response.status_code == 200:
                        history = history_response.json()
                        if prompt_id in history:
                            output_images = history[prompt_id]['outputs']
                            if output_images:
                                image_data = output_images['13']['images'][0]
                                image_url = f"{app.config['COMFYUI_API_URL']}/view?filename={image_data['filename']}"
                                
                                image_response = http_client.get(image_url)
                                if image_response.status_code == 200:
                                    # Sanitize prompts for use in headers
                                    safe_original_prompt = escape_html(original_prompt).replace('\n', ' ').replace('\r', '')
                                    safe_improved_prompt = escape_html(improved_prompt).replace('\n', ' ').replace('\r', '')
                                    
                                    return Response(
                                        image_response.content,
                                        mimetype=image_response.headers['Content-Type'],
                                        headers={
                                            'X-Original-Prompt': safe_original_prompt,
                                            'X-Improved-Prompt': safe_improved_prompt,
                                            'Access-Control-Expose-Headers': 'X-Original-Prompt, X-Improved-Prompt'
                                        }
                                    )
                except requests.exceptions.RequestException:
                    return jsonify({'error': 'Failed to fetch image generation history'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Unable to connect to ComfyUI API. Make sure it\'s running.'}), 503

    return jsonify({'error': 'Failed to generate image'}), 500

@app.route('/api/setup', methods=['POST'])
def save_setup():
    data = request.json
    app.config['LLM_CONFIG'] = {
        'choice': data['llmChoice'],
        'model': data.get('ollamaModel') or data.get('modelName'),
        'api_key': data.get('apiKey')
    }
    llm_service.update_config(app.config['LLM_CONFIG'])
    return jsonify({'message': 'Setup saved successfully'})

@app.route('/api/setup', methods=['GET'])
def get_setup():
    return jsonify(app.config.get('LLM_CONFIG', {'choice': None}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)