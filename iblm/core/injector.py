from typing import Any, Dict, List


def _top_preference(preferences: Dict[str, Dict[str, float]], key: str) -> str | None:
    values = preferences.get(key, {})
    if not values:
        return None
    return max(values.items(), key=lambda item: item[1])[0]


def build_system_prompt(brain: Dict[str, Any]) -> str:
    lines: List[str] = ["SYSTEM:", "User Profile:"]
    preferences = brain.get("preferences", {})
    style = brain.get("style", {})

    language = None
    if isinstance(preferences, dict):
        language = _top_preference(preferences, "language")
        if language:
            if preferences["language"].get(language, 0.0) >= 0.5:
                lines.append(f"- Preferred language: {language}")

    if style.get("concise", 0.0) >= 0.5:
        lines.append("- Communication style: concise")
    if style.get("verbose", 0.0) >= 0.5:
        lines.append("- Communication style: verbose")

    if language and language != "Python" and preferences["language"].get(language, 0.0) >= 0.5:
        lines.append("- Avoid Python unless explicitly requested")

    lines.append("")
    lines.append("Follow this profile strictly.")
    lines.append("Rules:")
    return "\n".join(lines)
