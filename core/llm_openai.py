import os, json
from typing import Dict
from openai import OpenAI

def oai_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def chat_json(system: str, user: str, model: str = None) -> Dict:
    model = model or os.environ.get("DEFAULT_OPENAI_MODEL", "gpt-4o-mini")
    client = oai_client()
    msg = client.chat.completions.create(
        model=model,
        response_format={"type":"json_object"},
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}],
        temperature=0.2,
    )
    return json.loads(msg.choices[0].message.content)
