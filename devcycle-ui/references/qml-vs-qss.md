# QML vs QSS — choosing how to style a PySide6 app

Qt offers two distinct UI/styling worlds. Pick one as the primary; you rarely
mix them inside the same window.

## QML (Qt Quick + Quick Controls 2)
- Declarative UI in `.qml`; styled via **Quick Controls styles**: `Basic`,
  `Fusion`, `Material`, `Universal`, `macOS`, `iOS`.
- Best for: new apps, fluid animation, touch, heavily custom/branded visuals,
  Material/Fluent looks with an accent color.
- Theming = set the style once + use `Material`/`Universal` attached properties,
  and a `Theme.qml` singleton for tokens.
- Python wires a backend `QObject` into the QML engine.

## QSS (Qt Style Sheets on QWidgets)
- Imperative widgets (`QPushButton`, `QTableView`, …) styled with a **CSS-like**
  stylesheet string.
- Best for: existing QWidgets apps, classic desktop tools, data-dense
  forms/tables, surgical restyles of native widgets.
- Theming = one global `.qss` + a matching `QPalette` (set both before `show()`).

## Decision cheatsheet

| Question | QML | QSS |
|---|---|---|
| Greenfield app? | ✅ | ➖ |
| Existing QWidgets codebase? | ➖ | ✅ |
| Want Material/Fluent + accent out of the box? | ✅ | ⚠️ (manual) |
| Heavy animation / custom-drawn controls? | ✅ | ➖ |
| Dense tables/forms, minimal restyle? | ➖ | ✅ |
| Need pixel-level control of native widgets? | ➖ | ✅ |
| Box-shadow / elevation? | ✅ (layers) | ⚠️ (QGraphicsDropShadowEffect) |

## Can they coexist?
- A QWidgets app can embed QML via `QQuickWidget` — but keep the QML island
  self-styled (its own Quick Controls style); QSS does **not** cascade into QML.
- Don't try to style the same control with both. Decide per window.

## Setting the style in Python

QML (before loading):
```python
from PySide6.QtQuickControls2 import QQuickStyle
QQuickStyle.setStyle("Material")   # or Universal / Fusion / Basic
```

QSS (at startup):
```python
app.setStyle("Fusion")                       # base widget style
app.setPalette(dark_palette)                 # see theming.md
app.setStyleSheet(open("theme.qss").read())  # then the stylesheet
```
