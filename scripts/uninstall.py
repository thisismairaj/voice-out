"""Undo the OS-level setup: stop the listener and remove the Startup
shortcut. Does not touch config.json, so re-running setup.py later restores
prior settings.

Usage: python uninstall.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

STARTUP_DIR = (
    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows"
    / "Start Menu" / "Programs" / "Startup"
)
SHORTCUT_PATH = STARTUP_DIR / "voice-out-spacebar-listener.lnk"


def main() -> int:
    subprocess.run(
        [sys.executable, str(Path(__file__).parent / "stop_listener.py")],
        capture_output=True,
    )
    if SHORTCUT_PATH.exists():
        SHORTCUT_PATH.unlink()
        print("voice-out: removed the Startup shortcut and stopped the listener.")
    else:
        print("voice-out: listener stopped (no Startup shortcut was found).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
