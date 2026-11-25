# Heimdall Cheat Bounty — headless/background process survival finding

## Finding

Heimdall's blanket "windowed-not-allowed" app-kill sweep decides what to terminate based solely on
whether a running process is registered with macOS as a regular, windowed, Dock-visible application
(`NSApplication.ActivationPolicy === 0` / "regular"). A process that never registers with AppKit at
all — no window, no Dock icon, no menu bar presence — is structurally outside what that check can see,
so it is never evaluated and never killed.

This is not a timing race or a one-off glitch: it is a property of what the check looks at. Any process
that does not create a window is invisible to it, regardless of language or runtime.

## What this PoC does, and does not do

Three independent, minimal programs — a Python script, a compiled C binary, and a bash shell script —
each do exactly one thing: write a timestamped heartbeat line to a local log file every 30 seconds.
None of them:
- create a window or register any AppKit/UI presence
- make network calls
- read the clipboard or capture input
- display, speak, or relay any exam content
- interact with Heimdall, Athena, or exam content in any way

They exist only to prove survival through a real proctored session, nothing else. This is a detection
gap, not a demonstrated answer-delivery exploit — no mechanism for getting exam content onto the
screen or into the student's hands was built or is implied by this PoC.

## Files

| File | What it is |
|---|---|
| `poc.py` | Python heartbeat script |
| `poc.c` | C source for the compiled-binary variant |
| `poc.sh` | Bash shell-script variant |
| `heimdall_poc_survival.log` | Live log from two real contest-window runs of `poc.py` |
| `heimdall_poc_c.log` | Live log from the compiled C binary |
| `heimdall_poc_shell.log` | Live log from the shell script |

## How it was tested

Each program was launched with `nohup <program> > /dev/null 2>&1 &` on an unmanaged macOS laptop, with
Athena running a live, fullscreen-locked proctored session (the real "windowed-not-allowed" kill-sweep
active, confirmed via the installed app's own source at `/Applications/Newton Athena.app`). All three
processes were confirmed alive via `ps aux` throughout, and the logs show continuous ~30s heartbeats
with no `STOP` line (other than a deliberate, intentional restart), meaning none were ever terminated
by Athena's app-kill logic.

## Root cause (confirmed against the live installed binary, not just the recovered source copy)

Verified by extracting the live, currently-installed `app.asar` from `/Applications/Newton Athena.app`
and `/Applications/Heimdall.app` (via `npx asar extract`, read-only) and reading the kill-sweep logic
directly: the blanket kill only targets processes where `activationPolicy === 0`. A process with no
AppKit registration, or one running with an accessory/background policy, falls outside that condition
entirely.
