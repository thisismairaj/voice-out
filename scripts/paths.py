"""Shared paths: plugin code lives wherever Claude Code installs it, but
per-user runtime state (config, pid files) needs a fixed writable location
that survives plugin updates/reinstalls, so it's kept separate in the user's
home directory instead of next to the code.
"""
from pathlib import Path

DATA_DIR = Path.home() / ".claude" / "voice-out"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = DATA_DIR / "config.json"
CURRENT_SPEECH_PID = DATA_DIR / "current_speech.pid"
LISTENER_PID = DATA_DIR / "listener.pid"

DEFAULT_CONFIG = {
    "enabled": True,
    "backend": "sapi",
    "sapi_voice": "Microsoft Zira Desktop",
    "sapi_rate": 0,
    "hold_threshold_seconds": 0.6,
}
