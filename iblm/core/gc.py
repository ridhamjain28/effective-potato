from typing import List, Dict, Any


def garbage_collect(raw_logs: List[str], signals: List[Dict[str, Any]]) -> None:
    raw_logs.clear()
    signals.clear()
