# Regression-test patterns (pytest + pytest-qt)

Load-on-demand companion to [SKILL.md](./SKILL.md) — concrete shapes for **step 3**
(write a failing regression test) and **steps 5/7** (run it). A regression test is
not just "a test for the fix": it must **fail for the bug's exact reason before the
fix and pass after**. If it passes before the fix, it doesn't pin the bug — rewrite
it until it goes red.

## Pick the layer (cheapest that reproduces the bug)

| Bug lives in… | Layer | Lives in | Needs `QApplication`? |
|---------------|-------|----------|------------------------|
| business rule / state / parsing / model | logic — `pytest` | `tests/unit/` | no |
| signal/slot, widget state, model↔view, enable/disable | widget — `pytest-qt` | `tests/widget/` | yes (via `qtbot`) |
| only reproduces driving the real window/OS | E2E — pywinauto | `tests/e2e/` | real desktop session |

Prefer the **logic** layer: if the bug only shows through a widget, that is usually
a smell that logic leaked into the UI — extract it so the regression can be a fast
unit test (this is the `devcycle-tdd` "thin widget / deep logic" rule).

## Anatomy of a regression test

```python
import pytest

# Reference the proven root cause so the test documents WHY it exists.
# (root cause: discount applied before tax → negative total on full refund)
def test_full_refund_does_not_produce_negative_total():
    cart = Cart(items=[Item(price=10_00, qty=1)])
    cart.apply_refund(amount=10_00)
    assert cart.total() == 0          # was -X before the fix (regression guard)
    assert cart.total() >= 0          # the criterion the bug violated
```

- Name it after the **behavior the bug broke**, not the function (`test_full_refund_…`,
  not `test_total_2`). It reads as the acceptance criterion you add back in Phase 1.
- Assert the **observable outcome**, not the internals you happened to change — the
  test must survive a future refactor (`devcycle-refine`).
- One regression test per confirmed root cause. Add more behaviors via the normal
  `devcycle-tdd` loop, not by overloading the guard.

## Reproduce a raised exception / crash

```python
import pytest

def test_parse_empty_config_raises_clear_error():
    with pytest.raises(ConfigError, match="empty config"):
        load_config("")            # before fix: bare KeyError / IndexError
```

For a value-corruption bug (no exception), assert the correct value directly — see
the cart example above.

## pytest-qt — widget-level regressions

`qtbot` is the fixture; it owns the event loop so you don't call `app.exec()`.

```python
# tests/widget/test_login_widget.py
def test_login_button_disabled_until_both_fields_filled(qtbot):
    w = LoginWidget()
    qtbot.addWidget(w)             # registers for cleanup — avoids crash-on-close
    assert not w.login_btn.isEnabled()

    w.user_edit.setText("dev.tester")
    qtbot.keyClicks(w.pass_edit, "secret")   # never hardcode a REAL credential here
    assert w.login_btn.isEnabled()
```

### Asserting a signal fires (the "signal never fires" bug class)

```python
def test_submit_emits_submitted_with_payload(qtbot):
    w = FormWidget()
    qtbot.addWidget(w)
    with qtbot.waitSignal(w.submitted, timeout=1000) as blocker:
        qtbot.mouseClick(w.submit_btn, Qt.LeftButton)
    assert blocker.args == ["dev.tester"]
```

Use `qtbot.assertNotEmitted(signal)` to pin a "signal fired when it shouldn't" bug.

### Async / debounced / timer behavior

```python
def test_status_clears_after_timeout(qtbot):
    w = StatusBar()
    qtbot.addWidget(w)
    w.flash("saved")
    assert w.text() == "saved"
    qtbot.waitUntil(lambda: w.text() == "", timeout=3000)   # not time.sleep()
```

Never `time.sleep()` in a Qt test — it blocks the event loop and the timer never
fires. Use `qtbot.waitUntil` / `qtbot.waitSignal`.

## Threading bugs (UI freeze / cross-thread access)

These rarely reproduce in a unit test — that's the bug. Pin them at the **logic
seam** instead: the worker that runs off the GUI thread should be a plain object
you can call directly.

```python
def test_export_worker_runs_without_touching_widgets():
    result = ExportWorker(rows).run()      # pure function — no QWidget in sight
    assert result.path.endswith(".csv")
```

Then the widget just connects `worker.finished` to a slot. If you *can't* write this
test without a widget, the fix isn't done — logic still lives on the GUI thread
(see the bug-shape table in [SKILL.md](./SKILL.md)).

## Run them (steps 5 & 7)

```powershell
pytest tests/unit -q                       # logic layer (fast)
pytest tests/widget -q                     # pytest-qt widget layer
pytest tests/unit/test_refund.py::test_full_refund_does_not_produce_negative_total -q
```

- **Step 3:** run the new test alone, confirm **RED** for the bug's reason.
- **Step 4:** apply the minimal fix, run again → **GREEN**.
- **Steps 5 & 7:** run the whole slice's suite, before *and* after the refactor.

## Anti-patterns

1. ❌ A regression test that is green before the fix — it pins nothing. Make it red first.
2. ❌ Asserting on a private attribute / the exact line you changed — breaks on refactor.
3. ❌ `time.sleep()` instead of `qtbot.waitSignal` / `waitUntil` — flaky or never fires.
4. ❌ Forgetting `qtbot.addWidget(w)` — widgets leak and tests crash on teardown.
5. ❌ Real credentials in a widget test — use throwaway literals; secrets live only in `.env.dev`.
6. ❌ Driving the real window when a logic test reproduces it — slow, and hides the leaked logic.
