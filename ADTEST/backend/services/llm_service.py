import requests
import logging
import json

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, config):
        self.config = config
        self.system_prompt = "You are a helpful assistant designed to improve image generation prompts. Your task is to enhance the given prompt to make the generated image more detailed and visually appealing."

    def improve_prompt(self, prompt):
        llm_choice = self.config.get('choice')
        logger.debug(f"Improving prompt with LLM choice: {llm_choice}")
        if llm_choice == 'ollama':
            improved_prompt = self._improve_prompt_with_ollama(prompt)
        elif llm_choice == 'cerebras':
            improved_prompt = self._improve_prompt_with_cerebras(prompt)
        elif llm_choice == 'sambanova':
            improved_prompt = self._improve_prompt_with_sambanova(prompt)
        elif llm_choice == 'groq':
            improved_prompt = self._improve_prompt_with_groq(prompt)
        else:
            logger.warning(f"Unsupported LLM choice: {llm_choice}. Using original prompt.")
            improved_prompt = prompt
        logger.debug(f"Improved prompt: {improved_prompt}")
        return improved_prompt

    def _improve_prompt_with_ollama(self, prompt):
        logger.debug(f"Improving prompt with Ollama using prompt: {prompt}")
        return self._generic_api_call(
            "Ollama",
            f"{self.config.get('api_url', '')}/api/generate",
            {'model': self.config.get('model'), 'system': self.system_prompt, 'prompt': prompt},
            self._parse_ollama_response
        )
    
    def _improve_prompt_with_cerebras(self, prompt):
        logger.debug(f"Improving prompt with Cerebras using prompt: {prompt}")
        return self._generic_api_call(
            "Cerebras",
            f"{self.config.get('api_url', '')}/v1/completions",
            {'model': self.config.get('model'), 'system': self.system_prompt, 'prompt': prompt},
            lambda r: r.json().get('choices', [{}])[0].get('text', prompt).strip()
        )

    # Implement similar changes for other methods if needed

    def _generic_api_call(self, service_name, url, payload, response_parser):
        logger.debug(f"Making API call to {service_name} with URL: {url} and payload: {payload}")
        try:
            response = requests.post(
                url,
                json=payload,
                headers={'Authorization': f"Bearer {self.config.get('api_key', '')}"},
                stream=True  # Enable streaming
            )
            response.raise_for_status()
            logger.debug(f"Response from {service_name}: {response.text}")  # Log the raw response content
            return response_parser(response)
        except requests.exceptions.HTTPError as e:
            logger.error(f"{service_name} API HTTP error: {e.response.status_code} - {e.response.text}")
            return payload['prompt']
        except requests.exceptions.ConnectionError as e:
            logger.error(f"{service_name} API connection error: {e}")
            return payload['prompt']
        except requests.exceptions.Timeout as e:
            logger.error(f"{service_name} API timeout error: {e}")
            return payload['prompt']
        except requests.exceptions.RequestException as e:
            logger.error(f"{service_name} API request error: {e}")
            return payload['prompt']
        except Exception as e:
            logger.error(f"Unexpected error in {service_name} API call: {e}")
            return payload['prompt']

    def _parse_ollama_response(self, response):
        improved_prompt = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_response = json.loads(line)
                    improved_prompt += json_response.get('response', '')
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response from Ollama: {e}")
                    logger.error(f"Response content: {line}")
        return improved_prompt.strip()

    def update_config(self, new_config):
        logger.debug(f"Updating LLM config to: {new_config}")
        self.config = new_config