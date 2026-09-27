"""Reusable pywinauto helpers for PySide6/Qt desktop E2E — copy to tests/e2e/.

These encode four realities that make naive pywinauto scripts hang or silently
fail against a Qt app. The conftest.py and tests import them; do NOT drive the app
with bare ``child_window(auto_id=...).click_input()`` — use these instead.

1. ACCESSIBILITY BRIDGE. Qt only publishes its widget tree to UI Automation when
   the accessibility bridge is active. conftest launches the app with
   ``QT_ACCESSIBILITY=1``; without it pywinauto sees an almost-empty window (just
   the title bar) and every ``.wait(...)`` blocks until timeout.

2. auto_id IS A DOTTED PATH. Qt reports the UIA AutomationId as a path such as
   ``App.MainWindow.QWidget...widgetCard.btnMenu`` whose LAST segment is the Qt
   objectName. So ``child_window(auto_id="btnMenu")`` never matches — match on the
   leaf segment via :func:`find_ctrl`.

3. NO PHYSICAL INPUT WHEN LOCKED. ``click_input``/``type_keys`` drive the real
   cursor/keyboard and fail ("SetCursorPos: file not found") when the session is
   locked/disconnected. Prefer the message-based UIA Invoke pattern (:func:`click`).

4. TEXT ENTRY VIA PASTE. ValuePattern (``set_edit_text``) does NOT fire Qt
   ``textChanged`` (so submit buttons that unlock on input stay disabled), and a
   custom password widget that keeps its real text in a private field ignores
   ValuePattern entirely (the app then sees an empty password). :func:`fill_edit`
   pastes (Ctrl+V) instead — it goes through Qt's normal input path, fires
   textChanged, handles special characters, then verifies and retries.
"""

from __future__ import annotations

import time


def leaf_id(wrapper) -> str:
    """Last dotted segment of a control's UIA AutomationId == its Qt objectName."""
    try:
        aid = wrapper.element_info.automation_id or ""
    except Exception:
        return ""
    return aid.split(".")[-1] if aid else ""


def safe_visible(wrapper) -> bool:
    try:
        return bool(wrapper.is_visible())
    except Exception:
        return False


def find_ctrl(scope, object_name, control_type=None, timeout=20,
              require_visible=True, index=0):
    """Return the control whose Qt objectName (auto_id leaf) == ``object_name``.

    Scans ``scope.descendants(...)`` (optionally filtered by ``control_type``) and
    matches the AutomationId leaf segment. ``index`` picks among duplicates (cards,
    list rows reuse objectNames). Raises TimeoutError if none appears in time.
    """
    deadline = time.time() + timeout
    kw = {"control_type": control_type} if control_type else {}
    last_err = None
    while time.time() < deadline:
        try:
            matches = [
                w for w in scope.descendants(**kw)
                if leaf_id(w) == object_name
                and (not require_visible or safe_visible(w))
            ]
            if len(matches) > index:
                return matches[index]
        except Exception as exc:  # transient UIA enumeration error
            last_err = exc
        time.sleep(0.4)
    raise TimeoutError(
        f"control objectName={object_name!r} (control_type={control_type}, "
        f"index={index}) not found within {timeout}s ({last_err})"
    )


def exists_ctrl(scope, object_name, control_type=None, timeout=3,
                require_visible=True) -> bool:
    try:
        find_ctrl(scope, object_name, control_type, timeout=timeout,
                  require_visible=require_visible)
        return True
    except TimeoutError:
        return False


def find_in_windows(windows, object_name, control_type=None, timeout=15,
                    require_visible=True):
    """Search several top-level windows for a control by objectName leaf.

    Use for controls that live in a SEPARATE top-level window — a login popup or a
    frameless Qt.Tool menu is not a descendant of the main window. ``windows`` is a
    zero-arg callable returning the windows to scan, e.g.::

        find_in_windows(lambda: list(app.windows()) + [main_window], "loginButton")
    """
    deadline = time.time() + timeout
    kw = {"control_type": control_type} if control_type else {}
    while time.time() < deadline:
        for win in windows():
            try:
                for w in win.descendants(**kw):
                    if leaf_id(w) == object_name and (
                        not require_visible or safe_visible(w)
                    ):
                        return w
            except Exception:
                continue
        time.sleep(0.4)
    raise TimeoutError(
        f"control objectName={object_name!r} not found in any top-level window "
        f"within {timeout}s"
    )


def click(ctrl) -> None:
    """Activate a control WITHOUT the physical mouse.

    Prefers the UIA Invoke pattern (message-based, needs no cursor / interactive
    desktop; a Qt button's InvokePattern fires its ``clicked`` signal). Falls back
    to a real click only if no message-based path works. Invoking a DISABLED
    control raises — wait with :func:`wait_enabled` first for gated buttons.
    """
    for attempt in (getattr(ctrl, "invoke", None), getattr(ctrl, "click", None)):
        if attempt is None:
            continue
        try:
            attempt()
            return
        except Exception:
            continue
    ctrl.click_input()  # last resort (needs an interactive desktop)


def wait_enabled(ctrl, timeout: int = 15) -> bool:
    """Wait until a control reports enabled (e.g. a submit button a field's
    textChanged unlocks). Returns False on timeout instead of raising."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if ctrl.is_enabled():
                return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def _set_clipboard(text: str) -> None:
    import win32clipboard
    import win32con
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    finally:
        win32clipboard.CloseClipboard()


def _focus(ctrl) -> None:
    for focus in (getattr(ctrl, "click_input", None),
                  getattr(ctrl, "set_focus", None)):
        if focus is None:
            continue
        try:
            focus()
            return
        except Exception:
            continue


def fill_edit(ctrl, value: str, attempts: int = 3) -> bool:
    """Populate an Edit by PASTING (focus -> select-all -> clear -> Ctrl+V), with
    verification and retry. Returns True once the value is in the field.

    Paste is used rather than ValuePattern (``set_edit_text``) on purpose — see the
    module docstring (fires textChanged; works with custom/masked password widgets;
    handles special characters). Verification: a password field masks with one dot
    per real char, so the accessible value's LENGTH equals the value length; a
    normal edit returns the literal text. Retrying absorbs focus/foreground races.
    """
    try:
        for _ in range(attempts):
            _focus(ctrl)
            try:
                _set_clipboard(value)
                ctrl.type_keys("^a{DEL}", set_foreground=True)
                ctrl.type_keys("^v", set_foreground=True)
            except Exception:
                try:  # last resort if paste is unavailable
                    ctrl.set_edit_text(value)
                    ctrl.type_keys("{END}{SPACE}{BACKSPACE}", set_foreground=True)
                except Exception:
                    pass
            time.sleep(0.25)
            try:
                current = ctrl.get_value() or ""
            except Exception:
                current = ""
            if len(current) == len(value):
                return True
        return False
    finally:
        # Never leave a pasted secret (e.g. APP_PASSWORD) lingering in the system
        # clipboard, where any app or clipboard manager could read it for the rest
        # of the session. Clear it once the field has been populated (any path out).
        try:
            _set_clipboard("")
        except Exception:
            pass
