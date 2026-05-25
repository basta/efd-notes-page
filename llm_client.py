"""Small helper to build an OpenAI-compatible client using opencode's auth.json.

Reads the API key from ~/.local/share/opencode/auth.json under the chosen provider,
falling back to an env var if set. Lets these scripts share whichever provider/model
opencode is configured with (currently `metacentrum` / `deepseek-v4-pro-thinking`).
"""

import json
import os
from openai import OpenAI

DEFAULT_PROVIDER = "metacentrum"
DEFAULT_BASE_URL = "https://llm.ai.e-infra.cz/v1"
DEFAULT_MODEL = "deepseek-v4-pro-thinking"
AUTH_PATH = os.path.expanduser("~/.local/share/opencode/auth.json")


def load_api_key(provider: str = DEFAULT_PROVIDER) -> str:
    env_var = f"{provider.upper()}_API_KEY"
    if os.getenv(env_var):
        return os.environ[env_var]
    if os.path.exists(AUTH_PATH):
        with open(AUTH_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        entry = data.get(provider)
        if isinstance(entry, dict) and entry.get("key"):
            return entry["key"]
    raise RuntimeError(
        f"No API key for provider '{provider}'. "
        f"Set {env_var} or add it to {AUTH_PATH}."
    )


def make_client(provider: str = DEFAULT_PROVIDER, base_url: str = DEFAULT_BASE_URL) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=load_api_key(provider))
