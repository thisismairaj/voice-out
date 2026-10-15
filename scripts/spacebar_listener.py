"""Background listener: if the spacebar is HELD DOWN for at least the
configured hold threshold anywhere on this machine, kill any voice-out
speech currently playing. A quick tap (normal typing) does nothing.

This is global, not scoped to Claude Code's own voice recording, because no
hook/signal exists for "the user started holding space to record." The hold
threshold is the mitigation: a deliberate hold-to-talk gesture is easy to
tell apart from a typed space by duration alone.

Run hidden via pythonw.exe (see /voice-out:setup, which wires up a Startup
folder shortcut). To stop the listener itself (not just the speech), use
stop_listener.py.
"""
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import keyboard  # noqa: E402
from paths import CONFIG_PATH, DEFAULT_CONFIG, LISTENER_PID  # noqa: E402
from voice_lib import kill_current_speech  # noqa: E402

_armed = False  # guards against spawning a new timer on every OS key-repeat event
_lock = threading.Lock()


def _hold_threshold() -> float:
    try:
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return float(cfg.get("hold_threshold_seconds", DEFAULT_CONFIG["hold_threshold_seconds"]))
    except Exception:
        return DEFAULT_CONFIG["hold_threshold_seconds"]


def _check_hold() -> None:
    time.sleep(_hold_threshold())
    if keyboard.is_pressed("space"):
        kill_current_speech()


def on_space_down(_event) -> None:
    global _armed
    with _lock:
        if _armed:
            return  # already timing this hold (key-repeat firing again)
        _armed = True
    threading.Thread(target=_check_hold, daemon=True).start()


def on_space_up(_event) -> None:
    global _armed
    with _lock:
        _armed = False


def main() -> None:
    import os
    LISTENER_PID.write_text(str(os.getpid()), encoding="ascii")
    keyboard.on_press_key("space", on_space_down, suppress=False)
    keyboard.on_release_key("space", on_space_up, suppress=False)
    try:
        keyboard.wait()  # blocks forever, listening
    finally:
        LISTENER_PID.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
