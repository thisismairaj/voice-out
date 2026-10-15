---
name: setup
description: One-time setup for voice-out - installs the keyboard dependency, picks a SAPI voice, wires up the Startup-folder spacebar listener, and starts it. Windows only. Run once after installing the plugin.
---

Run this exact command and relay its full output to the user verbatim:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py"
```

If it fails because `python`/`pythonw` isn't found, tell the user to install
Python 3.9+ from python.org with "Add python.exe to PATH" checked, then run
`/voice-out:setup` again.

If the output says this isn't Windows, tell the user plainly that voice-out
only works on Windows today - the speech backend (Windows SAPI) and the
global spacebar listener (a Startup-folder entry) are both Windows-specific
- and stop there.

Otherwise, summarize in one short sentence what's now live (voice, hold
threshold, and that the listener auto-starts on login), and mention
`/voice-out:toggle` and `/voice-out:stop` for day-to-day control.
