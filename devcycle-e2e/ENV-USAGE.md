# Wiring `.env.dev` into the E2E harness

How credentials, launch, and logs flow from `.env.dev` into a pywinauto run. The
contract (which keys exist) is in
[../devcycle/ENV-FORMAT.md](../devcycle/ENV-FORMAT.md); this is how the harness
consumes it.

## The flow

```
.env.dev ──env_loader.load_env()──▶ cfg dict
                                      │
   APP_SANDBOX ─────┐                 │
   APP_SANDBOX_ENV ─┴─▶ sandbox fixture builds a CHILD env block (isolated dirs)
                                      │   ↓ (app launched INSIDE the sandbox)
   APP_LAUNCH_CMD ──┐                 │
   APP_CWD ─────────┼─▶ subprocess.Popen(..., env=sandbox.env) ─▶ connect by pid
   APP_BACKEND ─────┘                 │
   QT_ACCESSIBILITY=1 ─▶ set in the child env so Qt exposes its widget tree
   APP_WINDOW_CLASS ─┐                │
   APP_WINDOW_TITLE ─┴▶ find the NEW top-level window after launch, connect pid
                                      │
   APP_USERNAME ──┐                   │
   APP_PASSWORD ──┴─▶ app_window fixture PASTES creds (ui_helpers.fill_edit)
                      + Invoke-clicks login (ui_helpers.click)
                                      │
   on failure:  APP_LOG_PATH ─▶ env_loader.tail_log() ─▶ failure report
                APP_LOG_TAIL_LINES ─▶ how many lines
```

## Sandbox: isolate the run (`APP_SANDBOX`)

By default (`APP_SANDBOX=on`) the `sandbox` fixture creates a fresh temp directory
and builds a **complete environment block for the child process** — it never
patches the pytest process's own `os.environ`, so a crashed test cannot strand the
runner pointing at a deleted directory. The `app` fixture spawns the app with
`subprocess.Popen(env=sandbox.env)` (pywinauto's `Application.start()` has no `env`
parameter, and the child would inherit ours). On teardown the temp dir is deleted.

```
%TEMP%\e2e_sandbox_XXXX\
├── Roaming\   (APPDATA)          ├── Local\  (LOCALAPPDATA)
├── Temp\      (TEMP/TMP/TMPDIR)  └── app\<APP_SANDBOX_ENV name>\  (config/data)
```

### Redirecting env vars is NOT enough — read this before trusting the sandbox

Two kinds of state on Windows are resolved through OS APIs that **ignore
environment variables entirely**:

| State | Resolved by | Redirecting `APPDATA` does… |
|-------|-------------|------------------------------|
| config / data dir | `platformdirs`, `QStandardPaths` → **known-folder API** | nothing |
| `QSettings(org, app)` | native store → **HKCU registry** | nothing |

An app that uses either will happily boot on the **real user's** config and
overwrite it during E2E. The only fix is to give the app an explicit escape hatch
that it reads from the environment, then name those vars in `APP_SANDBOX_ENV`:

```python
# config dir — src/config/config.py
app_base_dir = os.environ.get("FCD_CONFIG_DIR") or user_config_dir("fcdclient")

# QSettings — src/UDSClient.py, before any QSettings() is constructed
if settings_dir := os.environ.get("FCD_SETTINGS_DIR"):
    QSettings.setDefaultFormat(QSettings.IniFormat)          # off the registry
    QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, settings_dir)
```

```ini
APP_SANDBOX=on
APP_SANDBOX_ENV=FCD_CONFIG_DIR,FCD_SETTINGS_DIR
```

`tests/e2e/test_sandbox_isolation.py` is the guard: it launches a child with the
sandbox env, asks the app's own modules where they resolve to, and fails if any
path escapes the sandbox root or lands in `HKEY_*`. Run it before trusting a suite.

- **`TMPDIR` matters.** Python's `tempfile` reads `TMPDIR` *before* `TEMP`/`TMP`,
  and shells like Git Bash export it pointing at the host temp. The fixture
  redirects all three; drop `TMPDIR` and the app's log file lands on the real machine.
- **Logs:** point `APP_LOG_PATH` at a redirected var (e.g. `%TEMP%\app.log`). The
  failure hook calls `tail_log(environ=sandbox.env)`, so the tail resolves against
  the **child's** TEMP, not the host's.
- **First-run state:** the app boots against empty config, so the test must drive
  any first-run/onboarding dialogs — this is intentional (it exercises the real
  cold-start path from app open).
- **Network is NOT sandboxed.** The app still talks to whatever backend `.env.dev`
  points at. Use a dev account and a dev environment; the sandbox is defence in
  depth for local state, not a substitute.
- **Disable** with `APP_SANDBOX=off` to run against the real profile (e.g. to
  reproduce a profile-specific bug); the fixture then yields an inactive sandbox
  (`sandbox.active is False`) and redirects nothing.

## `env_loader.py` API

```python
from env_loader import load_env, tail_log, redacted

cfg = load_env()        # validates required keys, applies defaults, finds .env.dev
                        # by walking up from CWD. Raises if missing/invalid.
print(redacted(cfg))    # safe to print: APP_PASSWORD masked
print(tail_log(cfg))    # last APP_LOG_TAIL_LINES of APP_LOG_PATH, password masked
```

CLI:

```bash
python scripts/env_loader.py --check      # validate, exit 1 if bad
python scripts/env_loader.py --tail-log   # print the log tail (for devcycle-debug)
```

## Secret handling rules

- `env_loader.redacted()` and `tail_log()` mask `APP_PASSWORD`. Use them whenever
  you print config or logs.
- `ui_helpers.fill_edit` enters the password by clipboard **paste**, not per-key
  typing — Qt's custom password widget ignores UIA ValuePattern, and paste avoids
  emitting the secret as loggable keystrokes. It clears the clipboard's prior
  contents as part of the select-all+paste. Never write the password to the CSV.
- Never write `APP_PASSWORD` into a committed file, a test name, or a screenshot
  caption.

## If the app has no login

Delete the credential steps in the `app_window` fixture and return the main
`window` directly. `APP_USERNAME`/`APP_PASSWORD` can stay in `.env.dev` unused, or
be dropped from the required list in `env_loader.py`.

## Pointing tests at the log path

`devcycle-debug` and the failure hook both call `tail_log()`, which resolves
`APP_LOG_PATH`. It accepts either:

- a **file** (`...\app.log`) — tails that file, or
- a **directory** — tails the most recently modified `*.log` in it.

Environment variables and `~` in the path are expanded.
