"""Claude Code Stop hook entrypoint: speak the reply that was just finished.

Reads the hook's stdin JSON payload, pulls the last assistant text message
out of the session transcript, cleans it, and hands it to speak.py as a
detached background process so this hook returns immediately.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def last_assistant_text(transcript_path: str) -> str:
    path = Path(transcript_path)
    if not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("type") != "assistant":
            continue
        message = entry.get("message") or {}
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            joined = "\n".join(p for p in parts if p)
            if joined:
                return joined
    return ""


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0

    # Loop guard: never speak in response to a Stop hook's own stop.
    if payload.get("stop_hook_active"):
        return 0

    transcript_path = payload.get("transcript_path") or ""
    if not transcript_path:
        return 0

    text = last_assistant_text(transcript_path)
    if not text.strip():
        return 0

    clean = subprocess.run(
        [sys.executable, str(ROOT / "clean_text.py")],
        input=text, capture_output=True, text=True, encoding="utf-8",
    ).stdout

    if not clean.strip():
        return 0

    subprocess.run(
        [sys.executable, str(ROOT / "speak.py")],
        input=clean, text=True, encoding="utf-8",
        capture_output=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
