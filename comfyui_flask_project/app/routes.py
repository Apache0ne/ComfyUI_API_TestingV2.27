import requests
import time
from flask import Blueprint, render_template, request, jsonify, current_app
import base64
import json
import os

bp = Blueprint('main', __name__)

def parse_models_file(filename):
    categories = {}
    current_category = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_category = line[1:-1]
                categories[current_category] = []
            elif line and current_category:
                categories[current_category].append(line)
    return categories

def get_model_categories():
    ckp_models = parse_models_file('CKPmodels.txt')
    return list(ckp_models.keys())

def get_models_and_loras(category):
    ckp_models = parse_models_file('CKPmodels.txt')
    lora_models = parse_models_file('Lmodels.txt')
    return {
        'models': ckp_models.get(category, []),
        'loras': lora_models.get(category, [])
    }

@bp.route('/', methods=['GET'])
def index():
    categories = get_model_categories()
    return render_template('index.html', categories=categories)

@bp.route('/get_models_and_loras', methods=['POST'])
def get_models_and_loras_route():
    category = request.form.get('category')
    return jsonify(get_models_and_loras(category))

@bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    category = request.form.get('category')
    selected_model = request.form.get('model')
    selected_lora = request.form.get('lora')

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
                "text": prompt,
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
                "filename_prefix": "WEBTEST",
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

    api_url = current_app.config['COMFYUI_API_URL']
    response = requests.post(f"{api_url}/prompt", json={"prompt": workflow})
    
    if response.status_code == 200:
        prompt_id = response.json()['prompt_id']
        
        while True:
            history_response = requests.get(f"{api_url}/history/{prompt_id}")
            if history_response.status_code == 200:
                history = history_response.json()
                if prompt_id in history:
                    output_images = history[prompt_id]['outputs']
                    if output_images:
                        image_data = output_images['13']['images'][0]
                        image_b64 = base64.b64encode(requests.get(f"{api_url}/view?filename={image_data['filename']}").content).decode('utf-8')
                        return jsonify({'image': image_b64})
            
            time.sleep(0.5)
    
    return jsonify({'error': 'Failed to generate image'}), 500