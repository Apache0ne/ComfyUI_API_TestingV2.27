import requests
import time
import ollama
from flask import Blueprint, render_template, request, jsonify, current_app
import base64

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_prompt = request.form.get('prompt')
        selected_model = request.form.get('model')
        selected_category = request.form.get('category')
        
        ollama_response = ollama.generate(model="llama3.2", prompt=f"Refine this image prompt for better results: {user_prompt}")
        refined_prompt = ollama_response['response'].strip()
        
        workflow = {
            "3": {
                "inputs": {
                    "seed": 1113884446105075,
                    "steps": 4,
                    "cfg": 1,
                    "sampler_name": "dpmpp_sde",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["17", 0],
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
                    "text": refined_prompt,
                    "clip": ["17", 1]
                },
                "class_type": "CLIPTextEncode",
            },
            "7": {
                "inputs": {
                    "text": "text, watermark",
                    "clip": ["17", 1]
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
            },
            "17": {
                "inputs": {
                    "lora_name": "Rorschach1024.safetensors",
                    "strength_model": 1,
                    "strength_clip": 1,
                    "model": ["4", 0],
                    "clip": ["4", 1]
                },
                "class_type": "LoraLoader",
            }
        }

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
                            return jsonify({
                                    'image': image_b64,
                                    'user_prompt': user_prompt,
                                    'refined_prompt': refined_prompt
                                })
                time.sleep(0.5)
        
        return jsonify({'error': 'Failed to generate image'}), 500
    models = current_app.config['CHECKPOINT_MODELS']
    return render_template('index.html', models=models)