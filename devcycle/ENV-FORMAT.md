# `.env.dev` contract

A single file at the repo root that the `devcycle-e2e` and `devcycle-debug`
skills read. It is the **only** place credentials, launch instructions, and the
log path live — skills never hardcode these.

> **Security:** `.env.dev` contains real dev credentials. Confirm it is listed
> in `.gitignore` before the first commit. Never print the password value back
> to the user or into logs/screenshots.

## Required keys

| Key | Meaning | Example |
|-----|---------|---------|
| `APP_LAUNCH_CMD` | Command that starts the desktop app | `python -m myapp.main` or `C:\apps\MyApp\MyApp.exe` |
| `APP_WINDOW_TITLE` | Regex matching the **main window** title (pywinauto `title_re`) | `My App.*` |
| `APP_USERNAME` | Login user for E2E flows | `dev.tester` |
| `APP_PASSWORD` | Login password for E2E flows | `••••••` |
| `APP_LOG_PATH` | Log file, or directory of logs, read on any failure | `C:\Users\me\AppData\Local\MyApp\logs\app.log` |

## Optional keys

| Key | Default | Meaning |
|-----|---------|---------|
| `APP_CWD` | repo root | Working directory to launch the app from |
| `APP_BACKEND` | `uia` | pywinauto backend (`uia` or `win32`) |
| `APP_STARTUP_TIMEOUT` | `30` | Seconds to wait for the main window to appear |
| `APP_LOG_TAIL_LINES` | `200` | How many trailing log lines to read on failure |
| `APP_SANDBOX` | `on` | Run E2E in an isolated, disposable environment (redirect `APPDATA`/`LOCALAPPDATA`/`USERPROFILE`/`HOME`/`TEMP` into a temp dir, wiped per run; also overrides `USERNAME` so a single-instance guard doesn't forward-and-exit). Set `off` to use the real profile. |
| `APP_SANDBOX_ENV` | *(empty)* | Comma-separated extra env-var names the app uses for its config/data dir (e.g. `MYAPP_CONFIG_DIR,MYAPP_DATA_DIR`); each is redirected into the sandbox too |
| `APP_WINDOW_CLASS` | *(empty)* | Win32 class of the main window (e.g. `CustomMainWindow`). Set when the launcher spawns the GUI in a **child** process so the window isn't owned by the launched pid — the `app` fixture then finds the new window by class instead of title. Confirm via the probe in `devcycle-e2e/E2E-GUIDE.md`. |
| `APP_DOMAIN` | *(empty)* | Server/tenant domain the test enters on an add-server / connect screen, when login needs more than user+password. |

> **Sandbox + logs:** when `APP_SANDBOX=on`, write `APP_LOG_PATH` using one of the
> redirected vars (e.g. `%LOCALAPPDATA%\MyApp\logs\app.log`) so the failure log
> tail follows the app into the sandbox instead of reading a stale real-profile
> path.

> **No key for accessibility:** the `devcycle-e2e` harness sets `QT_ACCESSIBILITY=1`
> automatically when launching (Qt otherwise hides its widget tree from UI
> Automation). E2E also needs `Pillow` (screenshots) + `pywin32` (clipboard paste)
> installed, and a real **unlocked** desktop session.

## Example `.env.dev`

```dotenv
APP_LAUNCH_CMD=python -m myapp.main
APP_WINDOW_TITLE=My App.*
APP_USERNAME=dev.tester
APP_PASSWORD=changeme
APP_LOG_PATH=C:\Users\me\AppData\Local\MyApp\logs\app.log
APP_BACKEND=uia
APP_STARTUP_TIMEOUT=30
APP_LOG_TAIL_LINES=200
APP_SANDBOX=on
APP_SANDBOX_ENV=MYAPP_CONFIG_DIR,MYAPP_DATA_DIR
APP_LOG_PATH=%LOCALAPPDATA%\MyApp\logs\app.log
```

The helper `scripts/env_loader.py` (bundled with `devcycle-e2e`) parses this file
and validates that the required keys are present.
