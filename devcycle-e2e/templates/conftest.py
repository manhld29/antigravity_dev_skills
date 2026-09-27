"""pytest fixtures for devcycle desktop E2E (PySide6/Qt + pywinauto), CSV-driven.

Copy to tests/e2e/conftest.py (alongside ui_helpers.py, env_loader.py,
csv_results.py, cases.csv). Reads .env.dev via env_loader, launches the real app
in a disposable sandbox WITH the Qt accessibility bridge on, drives login, and —
for every test tagged @pytest.mark.case("TC-id") — captures a screenshot and
writes PASS/FAIL (+ a masked log tail on failure) back into the matching cases.csv
row.

Requires: pywinauto, pytest, Pillow (screenshots), pywin32 (clipboard paste).
Windows only; needs a real, UNLOCKED desktop session for the login keystrokes.
Read ui_helpers.py first — it explains the four Qt+UIA realities baked in here.
"""

from __future__ import annotations

import datetime as _dt
import importlib.util
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


def _load_sibling(mod_name: str, filename: str):
    """Import a helper vendored next to this conftest (or shipped with the skill)."""
    local = Path(__file__).with_name(filename)
    path = local if local.is_file() else (
        Path(__file__).resolve().parents[2]
        / "skills" / "dev-fcd" / "devcycle-e2e" / "scripts" / filename
    )
    if not path.is_file():
        raise FileNotFoundError(
            f"cannot load helper {filename!r}: not found next to conftest ({local}) "
            f"nor in the devcycle-e2e skill ({path})"
        )
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot create an import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


env_loader = _load_sibling("env_loader", "env_loader.py")
csv_results = _load_sibling("csv_results", "csv_results.py")

import ui_helpers as U  # noqa: E402  (leaf-id find / invoke-click / paste-fill)
from pywinauto import Application, Desktop  # noqa: E402
from pywinauto.timings import Timings, wait_until  # noqa: E402

Timings.window_find_timeout = 30

_ARTIFACTS = Path(__file__).with_name("_artifacts")
_CASES_CSV = Path(__file__).with_name("cases.csv")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "case(id): link this test to a row (case_id) in cases.csv"
    )


@pytest.fixture(scope="session")
def env() -> dict:
    """Validated .env.dev config (password masked when printed)."""
    return env_loader.load_env()


def _sandbox_env_names(env: dict) -> list[str]:
    raw = env.get("APP_SANDBOX_ENV", "") or ""
    return [n.strip() for n in raw.replace(";", ",").split(",") if n.strip()]


class Sandbox:
    """A disposable environment handed to the app under test.

    ``root`` is the temp dir every redirected path lives under; ``env`` is the
    COMPLETE environment block for the child process. Nothing here mutates the
    pytest process's own ``os.environ`` — isolation is applied at spawn time, so
    a crashed test can never leave the host runner pointing at a deleted dir.
    """

    def __init__(self, root: Path | None, child_env: dict[str, str]):
        self.root = root
        self.env = child_env

    @property
    def active(self) -> bool:
        return self.root is not None


@pytest.fixture
def sandbox(env):
    """Build the isolated environment block the app will be launched with.

    Three kinds of host state are redirected into a fresh temp dir:

    1. Profile dirs — APPDATA / LOCALAPPDATA / USERPROFILE / HOME / TEMP / TMP /
       TMPDIR. Covers ``tempfile.gettempdir()`` and ``os.path.expanduser("~")``.
       TMPDIR is not decorative: ``tempfile`` reads TMPDIR **before** TEMP/TMP, and
       a shell like Git Bash exports it pointing at the host's temp — overriding
       only TEMP/TMP would leave the app's log on the real machine.
    2. App-specific dirs named in APP_SANDBOX_ENV. This is the ONLY thing that
       isolates state resolved through an OS API that ignores env vars — the
       Windows KNOWN-FOLDER API behind platformdirs / QStandardPaths, and the
       HKCU registry behind a native QSettings(). Such an app must READ these
       vars for the redirect to take: give it an explicit escape hatch (e.g.
       `os.environ.get("APP_CONFIG_DIR") or user_config_dir(...)`, and
       `QSettings.setDefaultFormat(IniFormat)` + `QSettings.setPath(...)`),
       then list the var names in APP_SANDBOX_ENV. Without that, the app boots on
       the REAL user's config and an E2E run can overwrite it.
    3. Identity — USERNAME/LOGNAME/USER, so a single-instance guard keyed on the
       OS user (a per-user QLocalServer name) does not forward-and-exit into a
       real running instance.

    Qt's accessibility bridge is switched on in the same block (pywinauto sees an
    empty window without it). APP_SANDBOX=off yields an inactive sandbox that
    runs against the real profile.

    Deleted on teardown, which runs AFTER the `app` fixture has killed the app.
    """
    child_env = dict(os.environ)
    child_env["QT_ACCESSIBILITY"] = "1"
    child_env["QT_ENABLE_ACCESSIBILITY"] = "1"

    disabled = str(env.get("APP_SANDBOX", "on")).strip().lower()
    if disabled in ("off", "0", "false", "no", ""):
        yield Sandbox(None, child_env)
        return

    root = Path(tempfile.mkdtemp(prefix="e2e_sandbox_"))
    dir_overrides: dict[str, Path] = {
        "APPDATA": root / "Roaming", "LOCALAPPDATA": root / "Local",
        "USERPROFILE": root, "HOME": root,
        "TEMP": root / "Temp", "TMP": root / "Temp", "TMPDIR": root / "Temp",
    }
    for name in _sandbox_env_names(env):
        dir_overrides[name] = root / "app" / name
    for target in dir_overrides.values():
        target.mkdir(parents=True, exist_ok=True)

    uniq = "e2e_" + root.name[-8:]
    child_env.update({k: str(v) for k, v in dir_overrides.items()})
    child_env.update({"USERNAME": uniq, "LOGNAME": uniq, "USER": uniq})

    try:
        yield Sandbox(root, child_env)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _kill_tree(pid: int) -> None:
    """Kill a pid and its children (a launcher may spawn the GUI as a child)."""
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(pid)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )


@pytest.fixture
def app(sandbox, env):
    """Launch the app inside the sandbox and yield (Application, window).

    Spawned with ``subprocess.Popen(env=sandbox.env)`` rather than pywinauto's
    ``Application.start()``: only an explicit environment block gives the child a
    redirected profile without the test runner inheriting it too (Application.start
    exposes no `env` parameter, and the child would inherit ours).

    Two launch quirks are handled:
    - We never WaitForInputIdle: launching via `python ...` (a console process)
      makes it raise 1471 ("not a GUI process"); we sync on the window instead.
    - The launcher may spawn the GUI in a CHILD process (venv stub), so the window
      is not owned by the pid we started. We find the NEW top-level window that
      appears after launch (by class name, else title) and connect to its pid.
    """
    cwd = env.get("APP_CWD") or None
    timeout = int(env["APP_STARTUP_TIMEOUT"])
    backend = env["APP_BACKEND"]
    win_class = env.get("APP_WINDOW_CLASS", "").strip()
    title_re = env["APP_WINDOW_TITLE"]

    def _match(w) -> bool:
        try:
            if win_class:
                return (w.element_info.class_name or "") == win_class
            import re
            return bool(re.search(title_re, w.element_info.name or ""))
        except Exception:
            return False

    def _pids() -> set:
        return {w.element_info.process_id
                for w in Desktop(backend=backend).windows() if _match(w)}

    before = _pids()
    launcher = subprocess.Popen(
        env["APP_LAUNCH_CMD"], cwd=cwd, env=sandbox.env,
        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
    )

    def _new_pid():
        fresh = _pids() - before
        return sorted(fresh)[-1] if fresh else None

    try:
        wait_until(timeout, 0.5, lambda: _new_pid() is not None)
    except Exception:
        _kill_tree(launcher.pid)
        raise AssertionError(
            f"No new app window appeared within {timeout}s. The launch may have "
            "forwarded to an already-running instance (single-instance guard), or "
            "the app failed to start — check the app log and APP_WINDOW_CLASS/TITLE."
        )

    gui_pid = _new_pid()
    application = Application(backend=backend).connect(process=gui_pid, timeout=timeout)
    window = (application.window(class_name=win_class) if win_class
              else application.window(title_re=title_re))
    window.wait("visible", timeout=timeout)
    yield application, window

    _kill_tree(gui_pid)
    _kill_tree(launcher.pid)


@pytest.fixture
def app_window(app, env):
    """(application, window) after logging in with .env.dev credentials.

    GENERIC login (adjust objectNames to your app; delete if there is no login).
    Uses ui_helpers so it survives Qt's dotted auto_id, a locked session (invoke
    clicks), and password fields (paste). If your login screen is a separate popup
    window, wrap the field lookups in U.find_in_windows(_scopes, ...). For a
    multi-screen route (server list -> card -> login, first-run onboarding, etc.),
    make this adaptive: branch on which control is visible — see E2E-GUIDE.md.
    """
    application, window = app

    def _scopes():
        try:
            return list(application.windows()) + [window]
        except Exception:
            return [window]

    user = U.find_in_windows(_scopes, "usernameEdit", "Edit", timeout=25)
    U.fill_edit(user, env["APP_USERNAME"])
    U.fill_edit(U.find_in_windows(_scopes, "passwordEdit", "Edit", timeout=10),
                env["APP_PASSWORD"])
    login_btn = U.find_in_windows(_scopes, "loginButton", "Button", timeout=10)
    U.wait_enabled(login_btn, 15)   # unlocks only after the fields' textChanged
    U.click(login_btn)

    # Confirm we're in: wait for a known post-login control (adjust objectName).
    U.find_ctrl(window, "mainContent", timeout=30)
    return application, window


# --- capture a screenshot per case + record the result back into cases.csv ---
def _case_id(item) -> str | None:
    marker = item.get_closest_marker("case")
    return str(marker.args[0]) if marker and marker.args else None


def _window_of(item):
    # add any fixture that yields (application, window) or a window
    for name in ("login_history_page", "app_window", "app"):
        val = item.funcargs.get(name)
        if val is None:
            continue
        return val[1] if isinstance(val, tuple) else val
    return None


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return  # only act on the test body, not setup/teardown

    case_id = _case_id(item)
    _ARTIFACTS.mkdir(parents=True, exist_ok=True)

    # 1. screenshot — for EVERY completed case (needs Pillow), named by case_id
    shot_rel = ""
    window = _window_of(item)
    if window is not None:
        try:
            name = case_id or item.name
            shot = _ARTIFACTS / f"{name}.png"
            window.capture_as_image().save(shot)
            shot_rel = str(shot.relative_to(_ARTIFACTS.parent))
            report.sections.append(("E2E screenshot", str(shot)))
        except Exception as exc:  # pragma: no cover
            report.sections.append(("E2E screenshot", f"failed: {exc}"))

    # 2. result text — assertion message + masked app-log tail on failure
    if report.passed:
        status, actual = "PASS", "ok"
    elif report.failed:
        status = "FAIL"
        actual = (report.longreprtext or "assertion failed").strip()
        try:
            # Resolve APP_LOG_PATH against the sandbox's env: the app logged into
            # the redirected TEMP, not the host's. Read it before the sandbox
            # fixture tears the directory down (teardown runs after this hook).
            sbx = item.funcargs.get("sandbox")
            actual += "\n--- app log ---\n" + env_loader.tail_log(
                environ=sbx.env if sbx is not None else None
            )
        except Exception as exc:  # pragma: no cover
            actual += f"\n(log unavailable: {exc})"
    else:
        status, actual = "SKIPPED", (report.longreprtext or "").strip()

    if report.failed:
        report.sections.append(("E2E app log", actual))

    # 3. write back into the matching cases.csv row (keyed by case_id)
    if case_id:
        run_at = _dt.datetime.now().isoformat(timespec="seconds")
        try:
            wrote = csv_results.write_result(
                _CASES_CSV, case_id, status, actual, shot_rel, run_at
            )
            if not wrote:
                report.sections.append(
                    ("E2E cases.csv", f"no row for case_id {case_id} in {_CASES_CSV}")
                )
        except Exception as exc:  # pragma: no cover
            report.sections.append(("E2E cases.csv", f"write failed: {exc}"))
