"""Interrupt whatever voice-out is currently speaking.

Usage: python stop.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from voice_lib import kill_current_speech  # noqa: E402


def main() -> int:
    if kill_current_speech():
        print("voice-out: stopped.")
    else:
        print("voice-out: nothing is speaking right now.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
