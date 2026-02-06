# framework/backends.py
import json
import requests
from openai import OpenAI

SYSTEM_JSON_ONLY = (
    "Return ONLY a single valid JSON object. "
    "No explanations. No markdown. No code fences."
)

class LlamaLocalBackend:
    def __init__(self, model="llama3", url="http://localhost:11434/api/chat"):
        self.model = model
        self.url = url

    def call(self, prompt: str) -> dict:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_JSON_ONLY},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 1200}
        }
        r = requests.post(self.url, json=payload, timeout=600)
        r.raise_for_status()
        text = r.json()["message"]["content"].strip()
        return json.loads(text)

class OpenAIBackend:
    def __init__(self, api_key: str, model="gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def call(self, prompt: str) -> dict:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_JSON_ONLY},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4000,
        )
        text = resp.choices[0].message.content.strip()
        return json.loads(text)

