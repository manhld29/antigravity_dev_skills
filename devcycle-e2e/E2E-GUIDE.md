# pywinauto E2E guide for PySide6/Qt apps

Reference for writing stable, non-flaky desktop E2E tests. SKILL.md gives the
workflow; this is the how-to. **Read this before writing tests** — the naive
pywinauto idioms (`child_window(auto_id=...)`, `click_input`, `set_edit_text`)
silently fail against Qt. Drive the app through [`ui_helpers.py`](templates/ui_helpers.py).

## The four Qt + UIA realities (learned the hard way)

These are baked into the templates; understand them so generated tests are correct.

1. **Accessibility bridge must be on.** Qt only publishes its widget tree to UI
   Automation when the accessibility bridge is active. The `app` fixture launches
   with `QT_ACCESSIBILITY=1` / `QT_ENABLE_ACCESSIBILITY=1`. Without it pywinauto
   sees an almost-empty window (just the title bar) and **every `.wait()` blocks
   until timeout** — the classic "test is stuck and never clicks anything".

2. **`auto_id` is a dotted PATH, not the objectName.** Qt reports the
   AutomationId as `App.MainWindow.QWidget...widgetCard.btnMenu`; the **last
   segment** is the Qt `objectName`. So `child_window(auto_id="btnMenu")` never
   matches. Use `U.find_ctrl(scope, "btnMenu", control_type="Button")`, which
   matches the leaf segment (and picks among duplicate objectNames by `index=`).

3. **Physical input fails on a locked/disconnected session.** `click_input` and
   `type_keys` drive the real cursor/keyboard and raise
   `SetCursorPos: file not found` (or silently go nowhere) when the desktop is
   locked. Click via the **UIA Invoke pattern** (`U.click`) — message-based, needs
   no cursor. A Qt button's InvokePattern fires its `clicked` signal.

4. **Enter text by PASTE, not ValuePattern.** `set_edit_text` (ValuePattern) does
   **not** fire Qt `textChanged`, so submit buttons that unlock on input stay
   disabled; and a custom masked-password widget keeps its real text in a private
   field that ValuePattern doesn't touch (→ the app sees an empty password).
   `U.fill_edit` pastes (Ctrl+V) — fires textChanged, populates password widgets,
   handles special chars — then verifies (masked len == value len) and retries.

## Backend & launch quirks

- **`backend="uia"`** (Qt exposes UIA; `win32` sees fewer controls). Set via `APP_BACKEND`.
- **`wait_for_idle=False`** when launching via `python …` (a console process) —
  else `WaitForInputIdle` raises 1471 ("not a GUI process").
- **Window ownership.** A venv/py launcher may spawn the GUI in a CHILD process, so
  the window isn't owned by `application.process`. The `app` fixture finds the NEW
  top-level window after launch — by **class name** (`APP_WINDOW_CLASS`, e.g.
  `CustomMainWindow`) if set, else by `APP_WINDOW_TITLE` regex — and connects to
  its pid. Confirm the real class with the probe below.
- **Single-instance guard.** If the app forwards a second launch to a running
  instance and exits, the fixture sees no new window. The sandbox overrides
  `USERNAME` (guards keyed on the OS user won't collide); otherwise close any
  running instance before the run.

## Selectors — trace from source, match by objectName leaf

**Make selectors stable in the app:** give every driven widget a unique
`objectName` (treat it as part of "done" in `devcycle-tdd`). A control with no
`objectName` is a code gap — add one, don't fall back to a brittle `title`.

### 1. Trace the route from the source (do this first)

Derive **which screens the test crosses and the action that opens each next
screen** from the code — don't assume:

```powershell
graphify path   "app launch" "<target screen>"   # the screen chain to the goal
graphify explain "<each screen on the chain>"     # what triggers each transition
```

Write the ordered route to `tests/e2e/route_<flow>.md` (screen · trigger control ·
arrival state). No code path to the target = a spec/code gap; raise it.

### 2. Confirm objectNames in the source, then map them

```powershell
graphify explain "<flow> screen"        # which module renders the screen
rg "setObjectName\(" -n src/            # exact objectNames + their file:line
```

Record each driven control in `tests/e2e/selectors.md` (screen · control ·
`objectName` · `control_type` · source `file:line`). Reference that map in tests.

### 3. Cross-check the live tree (fallback)

Confirm the source matches reality — objectNames, the window class, whether a popup
is a separate window — with a short probe (adapt paths):

```python
from pywinauto import Application, Desktop
import os; os.environ["QT_ACCESSIBILITY"] = "1"   # or nothing shows!
app = Application(backend="uia").start("<APP_LAUNCH_CMD>", work_dir="<APP_CWD>",
                                       wait_for_idle=False)
win = Desktop(backend="uia").window(title_re="<APP_WINDOW_TITLE>")
win.wait("visible", timeout=30)
print("class:", win.element_info.class_name)             # -> APP_WINDOW_CLASS
for d in win.descendants():
    aid = d.element_info.automation_id or ""
    if aid:                                              # leaf == objectName
        print(aid.split(".")[-1], d.element_info.control_type, d.window_text()[:30])
```

## Driving the app — always via ui_helpers

```python
import ui_helpers as U
btn  = U.find_ctrl(window, "saveButton", "Button", timeout=10)  # leaf-match, waits
U.click(btn)                                     # UIA Invoke (works when locked)
U.fill_edit(U.find_ctrl(window, "nameEdit", "Edit"), "value")   # paste + verify
U.wait_enabled(U.find_ctrl(window, "submit", "Button"))         # gated buttons
U.exists_ctrl(window, "savedToast", timeout=5)   # bool, for branching / negatives
```

- **Never** `time.sleep`. `find_ctrl`/`exists_ctrl` poll on state; `wait_enabled`
  waits for a button a field's textChanged unlocks (invoking a disabled control raises).
- **Separate windows** (login popup, frameless `Qt.Tool` menu, modal dialog) are
  NOT descendants of the main window — search across top-levels:
  ```python
  scopes = lambda: list(application.windows()) + [window]
  U.find_in_windows(scopes, "loginButton", "Button")
  ```
- **Menus** built as frameless Tool windows: invoke the item button by its
  objectName leaf via `find_in_windows`; click promptly (menus auto-close on focus loss).

### The step-by-step journey (adaptive)

Each test walks from app open to the asserted success, waiting on the state each
step produces. Because the app may **not** cold-start clean (config via the Windows
known-folder API isn't sandbox-isolated), branch on what's actually visible instead
of assuming a fixed first screen:

```python
application, window = app
if U.exists_ctrl(window, "btnAddServer", "Button", timeout=8):     # first-run/HOME
    U.click(U.find_ctrl(window, "btnAddServer", "Button"))
    U.fill_edit(U.find_ctrl(window, "inputDomain", "Edit", 20), env["APP_DOMAIN"])
    nxt = U.find_ctrl(window, "nextButton", "Button", 20)
    U.wait_enabled(nxt); U.click(nxt)
elif U.exists_ctrl(window, "widgetCard", timeout=8):               # has saved state
    ...  # click the card / its menu's Connect action to reuse a saved session
# then the login form (may be a popup), then wait for a post-login control...
```

## Tables and lists

```python
table = U.find_ctrl(window, "resultsTable", "Table")
assert any("expected" in r.window_text() for r in table.descendants(control_type="DataItem"))
```

## Flake checklist

```
[ ] App launched with QT_ACCESSIBILITY=1 (else the tree is empty)
[ ] Controls found via U.find_ctrl (objectName leaf), not child_window(auto_id=...)
[ ] Clicks via U.click (Invoke); text via U.fill_edit (paste); no time.sleep
[ ] Gated submit buttons awaited with U.wait_enabled before clicking
[ ] Popups/menus/dialogs searched across top-levels (find_in_windows)
[ ] Navigation adaptive to the real boot screen (config may not be isolated)
[ ] Every driven control has a unique objectName; missing = code gap
[ ] Negative paths covered (wrong input -> error, no false success)
[ ] No real/production credentials — dev account only
```

## Environment / session requirements

pywinauto drives the real window manager — it does **not** run truly headless.
UIA Invoke/enumeration work on a disconnected session, but the **password paste
needs an UNLOCKED interactive desktop** (Qt blocks UIA writes to password fields,
so keystrokes are the only path). For CI, use a Windows runner with an auto-logged-
in, unlocked interactive session (or a kept-alive RDP/VM). Also install `Pillow`
(screenshots) and `pywin32` (clipboard paste). Unit and `pytest-qt` widget tests
(from `devcycle-tdd`) are the headless-friendly layer; pywinauto E2E is on-machine.
