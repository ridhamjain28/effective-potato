import json
import unittest
from pathlib import Path

from iblm.adapters.local_adapter import LocalAdapter
from iblm.runtime.loop import create_state, run_cycle


class ScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.brain_path = Path(__file__).resolve().parents[1] / "brain.json"
        self.brain_path.write_text(
            json.dumps(
                {
                    "version": "0.1",
                    "style": {},
                    "preferences": {},
                    "rules": {},
                },
                indent=2,
            )
        )
        self.state = create_state()
        self.adapter = LocalAdapter()

    def test_scenario_1(self) -> None:
        run_cycle(self.state, self.adapter, "Use TypeScript")
        brain = json.loads(self.brain_path.read_text())
        self.assertIn("language", brain["preferences"])
        self.assertIn("TypeScript", brain["preferences"]["language"])

    def test_scenario_2(self) -> None:
        run_cycle(self.state, self.adapter, "Keep answers concise")
        brain = json.loads(self.brain_path.read_text())
        self.assertGreater(brain["style"].get("concise", 0.0), 0.5)

    def test_scenario_3(self) -> None:
        run_cycle(self.state, self.adapter, "Use TypeScript")
        run_cycle(self.state, self.adapter, "Use Python")
        run_cycle(self.state, self.adapter, "No, not Python")
        brain = json.loads(self.brain_path.read_text())
        python_score = brain["preferences"]["language"].get("Python", 0.0)
        ts_score = brain["preferences"]["language"].get("TypeScript", 0.0)
        self.assertLess(python_score, 0.4)
        self.assertGreaterEqual(ts_score, 0.9)

    def test_scenario_4(self) -> None:
        run_cycle(self.state, self.adapter, "Use TypeScript")
        run_cycle(self.state, self.adapter, "Keep answers concise")
        response = run_cycle(self.state, self.adapter, "Build a REST API")
        self.assertIn("TypeScript", response)
        self.assertNotIn("Python", response)
        self.assertLess(len(response), 200)


if __name__ == "__main__":
    unittest.main()
