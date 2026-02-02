from .base import BaseAdapter


class OpenAIAdapter(BaseAdapter):
    def call_llm(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError("OpenAI adapter not configured.")
