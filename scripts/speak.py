"""Dispatch cleaned text to the configured TTS backend, detached and
non-blocking, so the caller (the Stop hook) returns immediately.

Usage: python speak.py < cleaned_text.txt
Reads text from stdin, reads config.json for which backend/voice to use.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paths import CONFIG_PATH, DEFAULT_CONFIG  # noqa: E402
from voice_lib import kill_current_speech  # noqa: E402

ROOT = Path(__file__).parent


def load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return dict(DEFAULT_CONFIG)


def speak_sapi(text: str, cfg: dict) -> None:
    # Always kill any previous, still-running speech first so two replies
    # can never overlap, and the pid file always tracks the one true
    # currently-speaking process.
    kill_current_speech()
    script = ROOT / "speak_sapi.ps1"
    voice = cfg.get("sapi_voice", DEFAULT_CONFIG["sapi_voice"])
    rate = cfg.get("sapi_rate", 0)
    args = [
        "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", str(script), "-VoiceName", voice, "-Rate", str(rate),
    ]
    # CREATE_NO_WINDOW: no visible window, but (unlike DETACHED_PROCESS)
    # the process still gets a working console/stdio, which speak_sapi.ps1
    # needs for [Console]::In to actually read the piped text.
    CREATE_NO_WINDOW = 0x08000000
    proc = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
    )
    proc.stdin.write(text.encode("utf-8"))
    proc.stdin.close()


def main() -> int:
    text = sys.stdin.read()
    if not text.strip():
        return 0
    cfg = load_config()
    if not cfg.get("enabled", True):
        return 0
    backend = cfg.get("backend", "sapi")
    if backend == "sapi":
        speak_sapi(text, cfg)
    else:
        print(f"voice-out: unknown backend '{backend}'", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
