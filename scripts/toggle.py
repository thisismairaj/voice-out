"""Turn voice-out on or off.

Usage: python toggle.py [on|off]   (no arg = flip current state)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paths import CONFIG_PATH, DEFAULT_CONFIG  # noqa: E402


def main() -> int:
    try:
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        cfg = dict(DEFAULT_CONFIG)
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else None
    if arg == "on":
        cfg["enabled"] = True
    elif arg == "off":
        cfg["enabled"] = False
    else:
        cfg["enabled"] = not cfg.get("enabled", True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"voice-out: {'on' if cfg['enabled'] else 'off'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
