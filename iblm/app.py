from iblm.adapters.local_adapter import LocalAdapter
from iblm.runtime.loop import create_state, run_cycle


def main() -> None:
    state = create_state()
    adapter = LocalAdapter()
    while True:
        try:
            user_message = input("> ").strip()
        except EOFError:
            break
        if not user_message:
            continue
        response = run_cycle(state, adapter, user_message)
        print(response)


if __name__ == "__main__":
    main()
