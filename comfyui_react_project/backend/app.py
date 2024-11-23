from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import ollama
import os
from config import Config

app = Flask(__name__)
CORS(app)
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

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    original_prompt = data['prompt']
    category = data['category']
    selected_model = data['model']
    selected_lora = data.get('lora', '')

    llm_config = app.config['LLM_CONFIG']
    if llm_config['choice'] == 'ollama':
        improved_prompt = ollama.generate(model=llm_config['model'], prompt=f"Improve this image generation prompt: {original_prompt}")
        improved_prompt = improved_prompt['response'].strip()
    else:
        # Implement other LLM API calls here (SambaNova, Groq, Cerebras)
        improved_prompt = original_prompt  # Fallback if not implemented

    workflow = {
        "3": {
            "inputs": {
                "seed": 1113884446105075,
                "steps": 4,
                "cfg": 1,
                "sampler_name": "dpmpp_sde",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler",
        },
        "4": {
            "inputs": {
                "ckpt_name": selected_model
            },
            "class_type": "CheckpointLoaderSimple",
        },
        "5": {
            "inputs": {
                "width": 1024,
                "height": 1024,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
        },
        "6": {
            "inputs": {
                "text": improved_prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode",
        },
        "7": {
            "inputs": {
                "text": "text, watermark",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode",
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode",
        },
        "13": {
            "inputs": {
                "filename_prefix": "ComfyUI_API_Testing",
                "images": ["8", 0]
            },
            "class_type": "SaveImage",
        }
    }

    if selected_lora and selected_lora.lower() != 'none':
        workflow["17"] = {
            "inputs": {
                "lora_name": selected_lora,
                "strength_model": 1,
                "strength_clip": 1,
                "model": ["4", 0],
                "clip": ["4", 1]
            },
            "class_type": "LoraLoader",
        }
        workflow["3"]["inputs"]["model"] = ["17", 0]
        workflow["6"]["inputs"]["clip"] = ["17", 1]
        workflow["7"]["inputs"]["clip"] = ["17", 1]

    response = requests.post(f"{app.config['COMFYUI_API_URL']}/prompt", json={"prompt": workflow})

    if response.status_code == 200:
        prompt_id = response.json()['prompt_id']
        
        while True:
            history_response = requests.get(f"{app.config['COMFYUI_API_URL']}/history/{prompt_id}")
            if history_response.status_code == 200:
                history = history_response.json()
                if prompt_id in history:
                    output_images = history[prompt_id]['outputs']
                    if output_images:
                        image_data = output_images['13']['images'][0]
                        image_url = f"{app.config['COMFYUI_API_URL']}/view?filename={image_data['filename']}"
                        return jsonify({
                            'image_url': image_url,
                            'original_prompt': original_prompt,
                            'improved_prompt': improved_prompt
                        })
    
    return jsonify({'error': 'Failed to generate image'}), 500

@app.route('/api/setup', methods=['POST'])
def save_setup():
    data = request.json
    print('Received setup data:', data) # Add this line
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
    app.run(debug=True)
