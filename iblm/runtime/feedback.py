from typing import Any, Dict


def apply_feedback(brain: Dict[str, Any], user_message: str) -> None:
    lower = user_message.lower()
    if any(token in lower for token in ["thanks", "good", "great", "perfect"]):
        _adjust_all(brain, 0.05)
    if _is_correction(lower):
        return
    if any(token in lower for token in ["no", "wrong", "bad", "not"]):
        _adjust_all(brain, -0.1)


def _is_correction(lower: str) -> bool:
    return any(
        phrase in lower
        for phrase in [
            "not python",
            "no python",
            "not typescript",
            "no typescript",
            "not javascript",
            "no javascript",
            "not ts",
            "no ts",
        ]
    )


def _adjust_all(brain: Dict[str, Any], delta: float) -> None:
    for section in ("style", "preferences", "rules"):
        store = brain.get(section, {})
        for key in list(store.keys()):
            value = store[key]
            if isinstance(value, dict):
                for sub_key in list(value.keys()):
                    value[sub_key] = min(1.0, max(0.0, value[sub_key] + delta))
                    if value[sub_key] < 0.1:
                        value.pop(sub_key, None)
                if not value:
                    store.pop(key, None)
            else:
                store[key] = min(1.0, max(0.0, value + delta))
                if store[key] < 0.1:
                    store.pop(key, None)
