from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import ollama
import os
import html
from config import Config
from workflow_utils import edit_workflow, list_workflows

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)

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

@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    print("Endpoint /api/workflows called")
    workflows = list_workflows()
    print(f"Workflows found: {workflows}")
    return jsonify(workflows)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    print("Received data:", data)  # Log received data
    
    workflow_name = data.get('workflow')
    user_inputs = data.get('inputs', {})
    
    original_prompt = user_inputs.get('prompt', '')
    category = user_inputs.get('category', '')
    selected_model = user_inputs.get('selected_model', '')
    selected_lora = user_inputs.get('lora', '')

    llm_config = app.config['LLM_CONFIG']
    if llm_config['choice'] == 'ollama':
        improved_prompt = ollama.generate(model=llm_config['model'], prompt=f"Improve this image generation prompt: {original_prompt}")
        improved_prompt = improved_prompt['response'].strip()
    else:
        # Implement other LLM API calls here (SambaNova, Groq, Cerebras)
        improved_prompt = original_prompt  # Fallback if not implemented

    # Update user_inputs with improved prompt
    user_inputs['prompt'] = improved_prompt

    try:
        # Use the edit_workflow function to get a preprocessed workflow
        workflow = edit_workflow(workflow_name, user_inputs)
        print("Edited workflow:", workflow)
    except FileNotFoundError:
        return jsonify({'error': f'Workflow "{workflow_name}" not found'}), 404

    try:
        response = requests.post(f"{app.config['COMFYUI_API_URL']}/prompt", json={"prompt": workflow})
        if response.status_code == 200:
            prompt_id = response.json()['prompt_id']
            
            while True:
                try:
                    history_response = requests.get(f"{app.config['COMFYUI_API_URL']}/history/{prompt_id}")
                    if history_response.status_code == 200:
                        history = history_response.json()
                        if prompt_id in history:
                            output_images = history[prompt_id]['outputs']
                            if output_images:
                                # Find the first image output
                                image_data = next((node['images'][0] for node in output_images.values() if 'images' in node), None)
                                if image_data:
                                    image_url = f"{app.config['COMFYUI_API_URL']}/view?filename={image_data['filename']}"
                                    
                                    image_response = requests.get(image_url)
                                    if image_response.status_code == 200:
                                        # Sanitize prompts for use in headers
                                        safe_original_prompt = html.escape(original_prompt).replace('\n', ' ').replace('\r', '')
                                        safe_improved_prompt = html.escape(improved_prompt).replace('\n', ' ').replace('\r', '')
                                        
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
    print('Received setup data:', data)
    app.config['LLM_CONFIG'] = {
        'choice': data['llmChoice'],
        'model': data.get('ollamaModel') or data.get('modelName'),
        'api_key': data.get('apiKey')
    }
    return jsonify({'message': 'Setup saved successfully'})

@app.route('/api/setup', methods=['GET'])
def get_setup():
    return jsonify(app.config.get('LLM_CONFIG', {'choice': None}))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)