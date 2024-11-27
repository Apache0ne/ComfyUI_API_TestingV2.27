class ComfyUIService:
    def __init__(self, api_url):
        self.api_url = api_url

    def create_workflow(self, selected_model, selected_lora, improved_prompt):
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

        return workflow