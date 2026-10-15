"""Shared helpers for voice-out: killing whatever is currently speaking."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paths import CURRENT_SPEECH_PID  # noqa: E402


def kill_current_speech() -> bool:
    """Kill whatever process is currently speaking, if any. Returns True if
    something was actually killed, False if nothing was tracked/running."""
    if not CURRENT_SPEECH_PID.exists():
        return False
    pid = CURRENT_SPEECH_PID.read_text(encoding="ascii", errors="ignore").strip()
    CURRENT_SPEECH_PID.unlink(missing_ok=True)
    if not pid.isdigit():
        return False
    result = subprocess.run(
        ["taskkill", "/PID", pid, "/T", "/F"],
        capture_output=True, text=True,
    )
    return result.returncode == 0
