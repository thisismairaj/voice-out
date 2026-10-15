"""Stop the global spacebar listener itself (not just current speech).

Usage: python stop_listener.py
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paths import LISTENER_PID  # noqa: E402


def main() -> int:
    if not LISTENER_PID.exists():
        print("voice-out: spacebar listener isn't running.")
        return 0
    pid = LISTENER_PID.read_text(encoding="ascii", errors="ignore").strip()
    LISTENER_PID.unlink(missing_ok=True)
    if not pid.isdigit():
        print("voice-out: spacebar listener stopped.")
        return 0
    result = subprocess.run(["taskkill", "/PID", pid, "/T", "/F"], capture_output=True, text=True)
    if result.returncode == 0:
        print("voice-out: spacebar listener stopped.")
    else:
        print(f"voice-out: could not stop PID {pid} ({result.stderr.strip() or result.stdout.strip()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
