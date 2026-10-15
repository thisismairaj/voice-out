"""One-time OS-level setup for voice-out: installs the `keyboard` pip
dependency, writes a default config if none exists (picking the first
installed SAPI voice), creates the Startup folder shortcut for the spacebar
listener, and starts the listener.

Usage: python setup.py
Safe to re-run - it won't overwrite an existing config.json, and it
replaces (not duplicates) the Startup shortcut and the running listener.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from paths import CONFIG_PATH, DATA_DIR, DEFAULT_CONFIG, LISTENER_PID  # noqa: E402

SCRIPTS_DIR = Path(__file__).parent
STARTUP_DIR = (
    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows"
    / "Start Menu" / "Programs" / "Startup"
)
SHORTCUT_PATH = STARTUP_DIR / "voice-out-spacebar-listener.lnk"


def ensure_keyboard_package() -> None:
    try:
        import keyboard  # noqa: F401
        return
    except ImportError:
        pass
    print("voice-out: installing the 'keyboard' package...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--user", "keyboard"], check=True)


def list_sapi_voices() -> list:
    ps = (
        "Add-Type -AssemblyName System.Speech; "
        "(New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() "
        "| ForEach-Object { $_.VoiceInfo.Name }"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps],
        capture_output=True, text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def ensure_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    cfg = dict(DEFAULT_CONFIG)
    voices = list_sapi_voices()
    if voices:
        cfg["sapi_voice"] = voices[0]
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    return cfg


def pythonw_path() -> str:
    exe = Path(sys.executable)
    candidate = exe.with_name("pythonw.exe")
    return str(candidate) if candidate.exists() else "pythonw"


def create_startup_shortcut() -> None:
    STARTUP_DIR.mkdir(parents=True, exist_ok=True)
    listener = SCRIPTS_DIR / "spacebar_listener.py"
    ps = f"""
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut('{SHORTCUT_PATH}')
$shortcut.TargetPath = '{pythonw_path()}'
$shortcut.Arguments = '"{listener}"'
$shortcut.WorkingDirectory = '{SCRIPTS_DIR}'
$shortcut.Save()
"""
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps], check=True)


def restart_listener() -> None:
    if LISTENER_PID.exists():
        subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "stop_listener.py")],
            capture_output=True,
        )
    listener = SCRIPTS_DIR / "spacebar_listener.py"
    CREATE_NO_WINDOW = 0x08000000
    subprocess.Popen(
        [pythonw_path(), str(listener)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
    )


def main() -> int:
    if sys.platform != "win32":
        print(
            "voice-out: this plugin only supports Windows right now "
            "(SAPI speech and the Startup-folder listener are both Windows-specific)."
        )
        return 1

    ensure_keyboard_package()
    cfg = ensure_config()
    create_startup_shortcut()
    restart_listener()

    print("voice-out: setup complete.")
    print(f"  voice: {cfg.get('sapi_voice')}")
    print(f"  hold-to-interrupt threshold: {cfg.get('hold_threshold_seconds')}s")
    print(f"  data dir: {DATA_DIR}")
    print("  the spacebar listener is running now, and will auto-start on login.")
    print("  use /voice-out:toggle to turn speech on/off, /voice-out:stop to interrupt it manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
