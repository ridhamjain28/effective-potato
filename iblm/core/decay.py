from typing import Any, Dict


DECAY_RATE = 0.995


def apply_decay(brain: Dict[str, Any]) -> None:
    for section in ("style", "preferences", "rules"):
        store = brain.get(section, {})
        if isinstance(store, dict):
            for key in list(store.keys()):
                value = store[key]
                if isinstance(value, dict):
                    for sub_key in list(value.keys()):
                        value[sub_key] *= DECAY_RATE
                        if value[sub_key] < 0.1:
                            value.pop(sub_key, None)
                    if not value:
                        store.pop(key, None)
                elif isinstance(value, (int, float)):
                    store[key] = value * DECAY_RATE
                    if store[key] < 0.1:
                        store.pop(key, None)
