from pathlib import Path
from typing import Any, Dict

from iblm.adapters.base import BaseAdapter
from iblm.core.compiler import compile_signals
from iblm.core.decay import apply_decay
from iblm.core.gc import garbage_collect
from iblm.core.injector import build_system_prompt
from iblm.core.observer import observe
from iblm.core.state import RuntimeState
from iblm.runtime.feedback import apply_feedback


def run_cycle(state: RuntimeState, adapter: BaseAdapter, user_message: str) -> str:
    state.raw_logs.append(user_message)
    signals = observe(user_message)
    state.signals.extend(signals)
    compile_signals(state.brain, state.signals)
    apply_feedback(state.brain, user_message)
    apply_decay(state.brain)
    state.save_brain()
    system_prompt = build_system_prompt(state.brain)
    response = adapter.call_llm(system_prompt, user_message)
    garbage_collect(state.raw_logs, state.signals)
    return response


def create_state() -> RuntimeState:
    brain_path = Path(__file__).resolve().parents[1] / "brain.json"
    state = RuntimeState(brain_path)
    state.load_brain()
    return state
