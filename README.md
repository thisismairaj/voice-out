<h1 align="center">voice-out</h1>

<p align="center">
  Claude Code already lets you talk to it with <code>/voice</code>.<br/>
  This plugin makes it talk back - and lets you cut it off mid-sentence
  by holding the spacebar.
</p>

---

## What it does

- **Speaks every reply out loud** the moment Claude finishes it, using
  Windows' built-in SAPI speech synthesis (no API key, no network call,
  nothing leaves your machine). Code blocks, file paths, URLs, and markdown
  syntax are stripped down to clean spoken prose first, instead of being
  read aloud literally.
- **Hold the spacebar anywhere, for a configurable moment, to interrupt it.**
  This is deliberately global, not scoped to Claude Code's own window -
  there's no hook for "the user started holding space to talk," so a hold
  long enough to be clearly intentional is the signal instead of a quick
  typed space.
- **Interrupts itself automatically** the instant you submit a new prompt,
  so replies never pile up or talk over each other.

```
you:    (holds space, talks)
claude: (replies in text, as always, then speaks the reply aloud)
you:    (holds space again mid-reply)
claude: (stops talking immediately)
```

## Install

```
/plugin install voice-out --marketplace thisismairaj/voice-out
```

Then run the one-time setup:

```
/voice-out:setup
```

This installs the `keyboard` pip package if it's missing, picks a SAPI voice
installed on your machine, creates a Startup-folder entry so the spacebar
listener starts on login, and starts it immediately.

**Windows only.** The speech backend (SAPI via PowerShell's
`System.Speech`) and the spacebar listener (a Startup-folder shortcut) are
both Windows-specific. `/voice-out:setup` checks for this and tells you
plainly if it won't work on your machine.

**Requires Python 3.9+** on `PATH` (for `python`/`pythonw`).

## Commands

- `/voice-out:setup` - one-time install (see above). Safe to re-run.
- `/voice-out:toggle [on|off]` - turn spoken replies on or off.
- `/voice-out:stop` - interrupt whatever's speaking right now, without
  touching the keyboard.
- `/voice-out:uninstall` - stop the spacebar listener and remove its
  Startup-folder entry (does not remove the plugin itself).

## How it works

Two plugin-level hooks, wired automatically on install via `hooks/hooks.json`
- no manual edits to your own `settings.json` needed:

- **`Stop`** - reads the session transcript, pulls the last assistant
  message, strips it down to spoken prose (`scripts/clean_text.py`), and
  hands it to a detached PowerShell process running `System.Speech`
  (`scripts/speak_sapi.ps1`).
- **`UserPromptSubmit`** - kills whatever's currently speaking, so a new
  turn never overlaps the previous reply.

A separate, always-running background process
(`scripts/spacebar_listener.py`, started by `/voice-out:setup` and kept
alive across logins via a Startup-folder shortcut) watches for a held-down
spacebar anywhere on the system and kills current speech the same way. It's
the one piece that lives outside Claude Code's own process model, because
Claude Code has no hook for a physical key being held down.

Runtime state (your chosen voice, the hold threshold, PID files) lives in
`~/.claude/voice-out/`, not inside the plugin's own install directory -
`${CLAUDE_PLUGIN_ROOT}` changes on every plugin update, so nothing that
needs to persist is written there.

## Configuring

Edit `~/.claude/voice-out/config.json`:

```json
{
  "enabled": true,
  "backend": "sapi",
  "sapi_voice": "Microsoft Zira Desktop",
  "sapi_rate": 0,
  "hold_threshold_seconds": 0.6
}
```

`sapi_voice` must be one of the voices installed on your machine - run
`/voice-out:setup` again after installing a new one to re-pick. `sapi_rate`
is SAPI's own `-10` to `10` scale. `hold_threshold_seconds` controls how
long you need to hold space before it counts as an interrupt rather than a
normal typed space; the listener re-reads this live, no restart needed.

## Limitations

- Windows only - no macOS/Linux speech backend or listener yet.
- The spacebar listener is genuinely global, by necessity. Holding space in
  any other app, or while typing a normal space into Claude Code itself,
  will also interrupt speech if held past the threshold.
- Uses whichever classic SAPI voices are already installed on your machine
  - no bundled voice, no cloud TTS.

## License

MIT
