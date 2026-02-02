from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def call_llm(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError
