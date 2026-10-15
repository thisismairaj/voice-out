---
name: uninstall
description: Stop the spacebar listener and remove its Startup-folder auto-start entry. Does not uninstall the plugin itself. Use when the user wants to undo voice-out's OS-level setup.
---

Run:

```
python "${CLAUDE_PLUGIN_ROOT}/scripts/uninstall.py"
```

Relay its output, then tell the user that to remove the plugin itself they
should also run `claude plugin uninstall voice-out` (or the matching
marketplace-removal command) afterward.
