import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    COMFYUI_API_URL = 'http://127.0.0.1:8188/api'  # Adjust this if ComfyUI is running on a different port or host
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

    @staticmethod
    def load_checkpoint_models():
        models_file = os.path.join(os.path.dirname(__file__), 'CKPmodels.txt')
        if os.path.exists(models_file):
            with open(models_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return ['creapromptLightning_creapromtHypersdxlV1.safetensors']  # Default model if file doesn't exist

    CHECKPOINT_MODELS = load_checkpoint_models.__func__()