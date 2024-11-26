import requests
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, config):
        self.config = config

    def improve_prompt(self, prompt):
        llm_choice = self.config.get('choice')
        if llm_choice == 'ollama':
            return self._improve_prompt_with_ollama(prompt)
        elif llm_choice == 'cerebras':
            return self._improve_prompt_with_cerebras(prompt)
        elif llm_choice == 'sambanova':
            return self._improve_prompt_with_sambanova(prompt)
        elif llm_choice == 'groq':
            return self._improve_prompt_with_groq(prompt)
        else:
            logger.warning(f"Unsupported LLM choice: {llm_choice}. Using original prompt.")
            return prompt

    def _improve_prompt_with_ollama(self, prompt):
        return self._generic_api_call(
            "Ollama",
            f"{self.config.get('api_url', '')}/api/generate",
            {'model': self.config.get('model'), 'prompt': prompt},
            lambda r: r.json().get('response', prompt).strip()
        )

    def _improve_prompt_with_cerebras(self, prompt):
        return self._generic_api_call(
            "Cerebras",
            f"{self.config.get('api_url', '')}/v1/completions",
            {'model': self.config.get('model'), 'prompt': prompt},
            lambda r: r.json().get('choices', [{}])[0].get('text', prompt).strip()
        )

    def _improve_prompt_with_sambanova(self, prompt):
        # Implement SambaNova API call here
        return prompt

    def _improve_prompt_with_groq(self, prompt):
        # Implement Groq API call here
        return prompt

    def _generic_api_call(self, service_name, url, payload, response_parser):
        try:
            response = requests.post(
                url,
                json=payload,
                headers={'Authorization': f"Bearer {self.config.get('api_key', '')}"}
            )
            response.raise_for_status()
            return response_parser(response)
        except requests.exceptions.RequestException as e:
            logger.error(f"{service_name} API error: {e}")
            return payload['prompt']

    def update_config(self, new_config):
        self.config = new_config