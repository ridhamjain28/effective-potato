from .base import BaseAdapter


class LocalAdapter(BaseAdapter):
    def call_llm(self, system_prompt: str, user_message: str) -> str:
        response = ""
        if "Preferred language: TypeScript" in system_prompt:
            response = "TypeScript: ok."
        elif "Preferred language: JavaScript" in system_prompt:
            response = "JavaScript: ok."
        else:
            response = "OK."
        if "Communication style: concise" in system_prompt:
            return response
        return f"{response} {user_message}"
