#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""devcycle-ui render — preview a generated PySide6 UI from QML + QSS.

Loads a `.qml` view and/or applies a `.qss` stylesheet and shows the
resulting window, so a generated design can be *seen* (or screenshotted)
before it is wired into a feature slice.

Layering (see references/qml-vs-qss.md — QSS does NOT cascade into QML):
  * --qss FILE     QWidget host styled by the QSS stylesheet (the real
                   "render using the QSS stylesheet"). With no --qml it
                   shows a control gallery so the theme is visible.
  * --qml FILE     QML view via QQuickWidget (self-styled by its Quick
                   Controls style / Theme.qml tokens).
  * --qml + --qss  combined: the QML island is embedded in a QWidget
                   host whose chrome is styled by the QSS (shared tokens).

Options:
  --style NAME          base QWidget style (default: Fusion)
  --quick-style NAME    Quick Controls style for QML (e.g. Material)
  --title TEXT          window title
  --screenshot OUT.png  render, grab to PNG, then exit 0 (use in
                        auto/headless mode to produce an artifact)
  --size WxH            window size (default 960x640)

Requires PySide6 (already a dependency of the target app); reads no
secrets.
"""

import argparse
import sys
from pathlib import Path


def _require_pyside6():
    try:
        import PySide6  # noqa: F401
    except ImportError:
        raise SystemExit(
            "PySide6 is required to render the UI but is not installed.\n"
            "Install it in the target app's environment:\n"
            "    pip install PySide6\n"
            "(render_ui.py runs in the app's venv; the search CLI needs "
            "no deps.)"
        )


def _parse_size(text):
    try:
        w, h = text.lower().split("x")
        return int(w), int(h)
    except Exception:
        raise SystemExit(
            f"--size must look like 960x640, got: {text!r}"
        )


def _read(path_str, kind):
    path = Path(path_str)
    if not path.is_file():
        raise SystemExit(f"{kind} file not found: {path}")
    return path


def _control_gallery():
    """A small QWidget gallery so a QSS theme is visible without a view."""
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
        QCheckBox, QComboBox, QProgressBar, QGroupBox,
    )

    root = QWidget()
    root.setObjectName("Root")
    outer = QVBoxLayout(root)

    outer.addWidget(QLabel("<h2>QSS theme preview</h2>"))
    form = QGroupBox("Form")
    fl = QVBoxLayout(form)
    fl.addWidget(QLineEdit(placeholderText="Text input"))
    combo = QComboBox()
    combo.addItems(["Option A", "Option B", "Option C"])
    fl.addWidget(combo)
    fl.addWidget(QCheckBox("Enable feature"))
    outer.addWidget(form)

    row = QHBoxLayout()
    primary = QPushButton("Primary")
    primary.setObjectName("Primary")
    primary.setDefault(True)
    row.addWidget(primary)
    row.addWidget(QPushButton("Secondary"))
    disabled = QPushButton("Disabled")
    disabled.setEnabled(False)
    row.addWidget(disabled)
    outer.addLayout(row)

    bar = QProgressBar()
    bar.setValue(60)
    outer.addWidget(bar)
    outer.addStretch(1)
    return root


def build(args):
    _require_pyside6()
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

    # Quick Controls style must be set before any QML loads.
    if args.qml and args.quick_style:
        from PySide6.QtQuickControls2 import QQuickStyle
        QQuickStyle.setStyle(args.quick_style)

    app = QApplication.instance() or QApplication(sys.argv)
    if args.style:
        app.setStyle(args.style)

    qss_text = ""
    if args.qss:
        qss_text = _read(args.qss, "QSS").read_text(encoding="utf-8")
        app.setStyleSheet(qss_text)  # styles every QWidget, including the host

    if args.qml:
        from PySide6.QtQuickWidgets import QQuickWidget
        from PySide6.QtCore import QUrl

        qml_path = _read(args.qml, "QML")
        host = QWidget()
        host.setObjectName("Root")
        lay = QVBoxLayout(host)
        lay.setContentsMargins(0, 0, 0, 0)
        view = QQuickWidget()
        view.setResizeMode(QQuickWidget.SizeRootObjectToView)
        view.setSource(QUrl.fromLocalFile(str(qml_path.resolve())))
        if view.status() == QQuickWidget.Error:
            errs = "\n".join(str(e) for e in view.errors())
            raise SystemExit(f"QML failed to load:\n{errs}")
        lay.addWidget(view)
        top = host
    elif args.qss:
        top = _control_gallery()
    else:
        raise SystemExit("nothing to render — pass --qml and/or --qss")

    top.setWindowTitle(args.title or "devcycle-ui preview")
    top.resize(*_parse_size(args.size))
    return app, top


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Render/preview a PySide6 UI from QML + QSS."
    )
    p.add_argument("--qml", help="path to a .qml view")
    p.add_argument("--qss", help="path to a .qss stylesheet")
    p.add_argument(
        "--style", default="Fusion",
        help="base QWidget style (default: Fusion)",
    )
    p.add_argument(
        "--quick-style",
        help="Quick Controls style for QML (Material/Fusion/…)",
    )
    p.add_argument("--title", help="window title")
    p.add_argument(
        "--screenshot", help="render, grab to this PNG, then exit"
    )
    p.add_argument(
        "--size", default="960x640",
        help="WxH window size (default 960x640)",
    )
    args = p.parse_args(argv)

    if not args.qml and not args.qss:
        p.error("pass --qml and/or --qss")

    app, top = build(args)
    top.show()

    if args.screenshot:
        # Let the event loop lay out + paint a couple of frames, then grab.
        from PySide6.QtCore import QTimer

        out = Path(args.screenshot)
        out.parent.mkdir(parents=True, exist_ok=True)

        def _grab_and_quit():
            top.grab().save(str(out))
            print(f"saved screenshot: {out}")
            app.quit()

        QTimer.singleShot(300, _grab_and_quit)
        app.exec()
        return 0

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
