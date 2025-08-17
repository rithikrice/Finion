# utils/watsonx_client.py
import os
import httpx
import json

class _Resp:
    def __init__(self, text: str):
        self.text = text or ""

class WatsonxModel:
    """
    Minimal drop-in for google.generativeai.GenerativeModel:
    exposes generate_content(prompt) -> object with .text
    """
    def __init__(self):
        self.region = os.getenv("WATSONX_REGION", "us-south")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "")
        self.model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")
        self.version = os.getenv("WATSONX_API_VERSION", "2025-02-11")
        self.api_key = os.getenv("WATSONX_API_KEY", "")

    def _iam_token(self) -> str:
        r = httpx.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self.api_key,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=None,
        )
        r.raise_for_status()
        return r.json()["access_token"]

    def generate_content(self, prompt: str) -> _Resp:
        token = self._iam_token()
        url = f"https://{self.region}.ml.cloud.ibm.com/ml/v1/text/generation?version={self.version}"
        payload = {
            "input": prompt,
            "parameters": {"max_new_tokens": 512, "temperature": 0.7},
            "model_id": self.model_id,
            "project_id": self.project_id,
        }
        r = httpx.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
            timeout=None,
        )
        r.raise_for_status()
        data = r.json()

        # Be tolerant to response shapes; prefer common fields.
        text = None
        if isinstance(data, dict):
            if "results" in data and data["results"]:
                first = data["results"][0]
                text = (
                    first.get("generated_text")
                    or first.get("text")
                    or first.get("output")
                )
            text = text or data.get("generated_text") or data.get("output")
        if not text:
            text = json.dumps(data)

        return _Resp(text=text)
