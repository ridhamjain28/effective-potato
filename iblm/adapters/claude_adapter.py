from .base import BaseAdapter


class ClaudeAdapter(BaseAdapter):
    def call_llm(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError("Claude adapter not configured.")
