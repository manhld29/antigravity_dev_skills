"""Worked example: CSV-driven desktop E2E tests driven by pywinauto.

Copy into tests/e2e/ and adapt the objectNames to your app. Each test is generated
from one row of cases.csv and tagged with that row's case_id via @pytest.mark.case.
After the run, conftest.py captures a screenshot per case and writes PASS/FAIL back
into the matching cases.csv row.

Controls are located with ui_helpers, NEVER bare child_window(auto_id=...): Qt
reports auto_id as a dotted path whose last segment is the objectName, so
find_ctrl matches that leaf. Clicks go through UIA Invoke (U.click) so they work on
a locked session; text is entered by paste (U.fill_edit) so textChanged fires and
password fields populate. See ui_helpers.py for the why.

Cases under test (see cases.csv):
    TC-001  Login valid          -> dashboard greets the user
    TC-002  Login wrong password -> error shown, no dashboard
"""

from __future__ import annotations

import pytest

import ui_helpers as U


@pytest.mark.case("TC-001")
def test_login_shows_dashboard(app_window, env):
    """Then: the dashboard is visible and greets the logged-in user."""
    # `app_window` already performed login using .env.dev credentials.
    _application, window = app_window

    greeting = U.find_ctrl(window, "greetingLabel", "Text", timeout=10)
    assert env["APP_USERNAME"] in greeting.window_text()


@pytest.mark.case("TC-002")
def test_invalid_login_shows_error(app, env):
    """A negative-path example that does NOT use the auto-login fixture.

    Given the app is open, When the user submits a wrong password,
    Then an error message appears and the dashboard does not load.
    """
    application, window = app

    def _scopes():
        try:
            return list(application.windows()) + [window]
        except Exception:
            return [window]

    U.fill_edit(U.find_in_windows(_scopes, "usernameEdit", "Edit"),
                env["APP_USERNAME"])
    U.fill_edit(U.find_in_windows(_scopes, "passwordEdit", "Edit"),
                "definitely-wrong-password")
    U.click(U.find_in_windows(_scopes, "loginButton", "Button"))

    error = U.find_ctrl(window, "loginError", "Text", timeout=10)
    assert error.window_text().strip() != ""

    # the dashboard must NOT appear
    assert not U.exists_ctrl(window, "mainContent", timeout=3), (
        "dashboard should not load after a failed login"
    )
