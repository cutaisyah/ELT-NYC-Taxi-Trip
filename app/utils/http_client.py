import requests

class HttpClient:
    def get(self, url, **kwargs):
        return requests.get(url, **kwargs)
    
    def post(self, url, payload, **kwargs):
        return requests.post(url, payload, **kwargs)
    
    def put(self, url, payload, **kwargs):
        return requests.put(url, payload,  **kwargs)
    
    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)
