import requests

class HTTPClient:
    def get(self, url, **kwargs):
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP GET request failed: {e}")
            return None

    def post(self, url, **kwargs):
        try:
            response = requests.post(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP POST request failed: {e}")
            return None

    def put(self, url, **kwargs):
        try:
            response = requests.put(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP PUT request failed: {e}")
            return None

    def delete(self, url, **kwargs):
        try:
            response = requests.delete(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP DELETE request failed: {e}")
            return None