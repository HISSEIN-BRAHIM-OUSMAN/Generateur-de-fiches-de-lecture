import os, json, requests
from typing import Dict

def hf_chat_json(system: str, user: str, model: str = None) -> Dict:
    model = model or os.environ.get("DEFAULT_HF_MODEL",
                                    "meta-llama/Meta-Llama-3-8B-Instruct")
    token = os.environ["HF_API_TOKEN"]
    url = f"https://api-inference.huggingface.co/models/{model}"
    # Simple chat-style prompt
    prompt = f"<<SYS>>{system}<</SYS>>\n\n[INST]{user}[/INST]"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 1024,
                                                "temperature": 0.2,
                                                "return_full_text": False}}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    text = r.json()[0]["generated_text"]
    # Essayez d'extraire JSON
    start = text.find("{")
    end = text.rfind("}")
    content = text[start:end+1] if start != -1 and end != -1 else "{}"
    return json.loads(content)
