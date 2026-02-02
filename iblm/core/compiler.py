from typing import Any, Dict, List


def _apply_confidence(store: Dict[str, float], key: str, delta: float) -> None:
    current = store.get(key, 0.0)
    updated = min(1.0, max(0.0, current + delta))
    if updated < 0.1:
        store.pop(key, None)
    else:
        store[key] = updated


def _penalize_conflicts(store: Dict[str, float], active_key: str, penalty: float) -> None:
    for key in list(store.keys()):
        if key != active_key:
            store[key] = max(0.0, store[key] * (1.0 - penalty))
            if store[key] < 0.1:
                store.pop(key, None)


def compile_signals(brain: Dict[str, Any], signals: List[Dict[str, Any]]) -> None:
    style = brain.setdefault("style", {})
    preferences = brain.setdefault("preferences", {})
    rules = brain.setdefault("rules", {})

    for signal in signals:
        signal_type = signal.get("type")
        if signal_type == "STYLE":
            key = signal["key"]
            _apply_confidence(style, key, 0.6)
            _penalize_conflicts(style, key, 0.2)
        elif signal_type == "PREFERENCE":
            key = signal["key"]
            value = signal["value"]
            pref_store = preferences.setdefault(key, {})
            _apply_confidence(pref_store, value, 0.6)
            _penalize_conflicts(pref_store, value, 0.2)
        elif signal_type == "CORRECTION":
            key = signal["key"]
            value = signal["value"]
            pref_store = preferences.setdefault(key, {})
            if value in pref_store:
                pref_store[value] = max(0.0, pref_store[value] * 0.4)
                if pref_store[value] < 0.1:
                    pref_store.pop(value, None)
            for other_key in list(pref_store.keys()):
                if other_key != value:
                    pref_store[other_key] = max(pref_store[other_key], 0.95)
            rules.setdefault("corrections", {})[value] = 1.0

    for key in list(style.keys()):
        if style[key] < 0.1:
            style.pop(key, None)
    for pref_key, pref_store in list(preferences.items()):
        for value in list(pref_store.keys()):
            if pref_store[value] < 0.1:
                pref_store.pop(value, None)
        if not pref_store:
            preferences.pop(pref_key, None)
    for rule_key in list(rules.keys()):
        if not rules[rule_key]:
            rules.pop(rule_key, None)
