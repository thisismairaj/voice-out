---
name: toggle
description: Turn voice-out's spoken replies on or off. Use when the user asks to mute, silence, enable, or disable voice replies.
---

Run, passing through whatever argument the user gave (`on`, `off`, or
nothing to flip the current state):

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/toggle.py" <on|off|nothing>
```

Relay its output to the user as-is.
