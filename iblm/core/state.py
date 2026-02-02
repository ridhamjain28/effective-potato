import json
from pathlib import Path
from typing import Any, Dict, List


class RuntimeState:
    def __init__(self, brain_path: Path) -> None:
        self.brain_path = brain_path
        self.raw_logs: List[str] = []
        self.signals: List[Dict[str, Any]] = []
        self.brain: Dict[str, Any] = {}

    def load_brain(self) -> None:
        if self.brain_path.exists():
            self.brain = json.loads(self.brain_path.read_text())
        else:
            self.brain = {
                "version": "0.1",
                "style": {},
                "preferences": {},
                "rules": {},
            }
            self.save_brain()

    def save_brain(self) -> None:
        self.brain_path.write_text(json.dumps(self.brain, indent=2, sort_keys=True))
