import json
import os
from copy import deepcopy

WORKFLOW_DIR = os.path.join(os.path.dirname(__file__), "workflows")

def load_workflow(name):
    file_path = os.path.join(WORKFLOW_DIR, f"{name}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Workflow '{name}' not found")
    with open(file_path, 'r') as f:
        return json.load(f)

def save_workflow(name, workflow):
    file_path = os.path.join(WORKFLOW_DIR, f"{name}.json")
    with open(file_path, 'w') as f:
        json.dump(workflow, f, indent=2)

def preprocess_workflow(workflow, user_inputs):
    processed_workflow = deepcopy(workflow)
    
    # Find nodes by class_type
    ckpt_loader = next((node for node_id, node in processed_workflow.items() if node['class_type'] == 'CheckpointLoaderSimple'), None)
    ksampler = next((node for node_id, node in processed_workflow.items() if node['class_type'] == 'KSampler'), None)
    clip_encode_positive = next((node for node_id, node in processed_workflow.items() if node['class_type'] == 'CLIPTextEncode' and node.get('_meta', {}).get('title', '').lower() == 'clip text encode (prompt)'), None)
    empty_latent = next((node for node_id, node in processed_workflow.items() if node['class_type'] == 'EmptyLatentImage'), None)
    lora_loader = next((node for node_id, node in processed_workflow.items() if node['class_type'] == 'LoraLoader'), None)

    # Update CheckpointLoaderSimple
    if ckpt_loader:
        ckpt_loader['inputs']['ckpt_name'] = user_inputs.get('selected_model', ckpt_loader['inputs'].get('ckpt_name'))
        ckpt_loader_id = next(node_id for node_id, node in processed_workflow.items() if node == ckpt_loader)

    # Update KSampler
    if ksampler:
        ksampler['inputs'].update({
            'seed': user_inputs.get('seed', ksampler['inputs'].get('seed')),
            'steps': user_inputs.get('steps', ksampler['inputs'].get('steps')),
            'cfg': user_inputs.get('cfg', ksampler['inputs'].get('cfg')),
            'sampler_name': user_inputs.get('sampler_name', ksampler['inputs'].get('sampler_name')),
            'scheduler': user_inputs.get('scheduler', ksampler['inputs'].get('scheduler')),
            'denoise': user_inputs.get('denoise', ksampler['inputs'].get('denoise')),
        })

    # Update CLIPTextEncode for positive prompt
    if clip_encode_positive:
        clip_encode_positive['inputs']['text'] = user_inputs.get('prompt', clip_encode_positive['inputs'].get('text'))

    # Update EmptyLatentImage
    if empty_latent:
        empty_latent['inputs'].update({
            'width': user_inputs.get('width', empty_latent['inputs'].get('width')),
            'height': user_inputs.get('height', empty_latent['inputs'].get('height')),
            'batch_size': user_inputs.get('batch_size', empty_latent['inputs'].get('batch_size')),
        })

    # Update or add LoraLoader
    if user_inputs.get('lora') and user_inputs['lora'].lower() != 'none':
        if lora_loader:
            # Update existing LoraLoader
            lora_loader['inputs'].update({
                'lora_name': user_inputs['lora'],
                'strength_model': user_inputs.get('lora_strength_model', lora_loader['inputs'].get('strength_model', 1)),
                'strength_clip': user_inputs.get('lora_strength_clip', lora_loader['inputs'].get('strength_clip', 1)),
            })
        elif ckpt_loader:
            # Add new LoraLoader
            new_lora_id = str(max(int(k) for k in processed_workflow.keys()) + 1)
            processed_workflow[new_lora_id] = {
                'inputs': {
                    'lora_name': user_inputs['lora'],
                    'strength_model': user_inputs.get('lora_strength_model', 1),
                    'strength_clip': user_inputs.get('lora_strength_clip', 1),
                    'model': [ckpt_loader_id, 0],
                    'clip': [ckpt_loader_id, 1]
                },
                'class_type': 'LoraLoader',
                '_meta': {
                    'title': 'Load LoRA'
                }
            }
            
            # Update connections
            if ksampler:
                ksampler['inputs']['model'] = [new_lora_id, 0]
            if clip_encode_positive:
                clip_encode_positive['inputs']['clip'] = [new_lora_id, 1]

    return processed_workflow

def edit_workflow(name, user_inputs):
    workflow = load_workflow(name)
    edited_workflow = preprocess_workflow(workflow, user_inputs)
    return edited_workflow

def list_workflows():
    print(f"Searching for workflows in: {WORKFLOW_DIR}")
    workflows = []
    try:
        for filename in os.listdir(WORKFLOW_DIR):
            if filename.endswith('.json'):
                workflows.append(filename[:-5])
        print(f"Workflows found: {workflows}")
    except Exception as e:
        print(f"Error listing workflows: {str(e)}")
    return workflows