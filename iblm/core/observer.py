import time
from typing import Any, Dict, List


def _timestamp() -> int:
    return int(time.time())


def observe(text: str) -> List[Dict[str, Any]]:
    lower = text.lower()
    signals: List[Dict[str, Any]] = []

    if "concise" in lower or "brief" in lower:
        signals.append(
            {
                "type": "STYLE",
                "key": "concise",
                "value": True,
                "confidence": 0.8,
                "timestamp": _timestamp(),
            }
        )
    if "verbose" in lower or "detailed" in lower:
        signals.append(
            {
                "type": "STYLE",
                "key": "verbose",
                "value": True,
                "confidence": 0.8,
                "timestamp": _timestamp(),
            }
        )

    language_map = {
        "typescript": "TypeScript",
        "python": "Python",
        "javascript": "JavaScript",
        "ts": "TypeScript",
    }
    for token, language in language_map.items():
        if f"use {token}" in lower or f"prefer {token}" in lower:
            signals.append(
                {
                    "type": "PREFERENCE",
                    "key": "language",
                    "value": language,
                    "confidence": 0.9,
                    "timestamp": _timestamp(),
                }
            )

    if "not" in lower or "no" in lower:
        for token, language in language_map.items():
            if f"not {token}" in lower or f"no {token}" in lower:
                signals.append(
                    {
                        "type": "CORRECTION",
                        "key": "language",
                        "value": language,
                        "confidence": 0.95,
                        "timestamp": _timestamp(),
                    }
                )

    return signals
