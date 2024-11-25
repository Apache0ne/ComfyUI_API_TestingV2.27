import requests

class LLMService:
    def __init__(self, config):
        self.config = config

    def improve_prompt(self, prompt):
        llm_choice = self.config['choice']
        if llm_choice == 'ollama':
            return self._improve_prompt_with_ollama(prompt)
        # Add support for other LLMs here
        else:
            return prompt  # Fallback if not implemented

    def _improve_prompt_with_ollama(self, prompt):
        try:
            response = requests.post(
                'http://ollama-api-url/improve-prompt',
                json={'prompt': prompt},
                headers={'Authorization': f'Bearer {self.config["api_key"]}'}
            )
            if response.status_code == 200:
                return response.json().get('response', prompt).strip()
            else:
                return prompt
        except requests.exceptions.RequestException:
            return prompt

    def update_config(self, new_config):
        self.config = new_config