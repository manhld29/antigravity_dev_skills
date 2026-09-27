# QSS reference (Qt Style Sheets on QWidgets)

Load this when styling QWidgets. QSS is CSS-like but **not** CSS — mind the
differences noted below.

## Selectors

```css
QPushButton            { }      /* by type (and subclasses) */
QPushButton#saveBtn    { }      /* by objectName (setObjectName("saveBtn")) */
.QPushButton           { }      /* exact class only (no subclasses) */
QDialog QPushButton    { }      /* descendant */
QGroupBox > QCheckBox  { }      /* direct child */
QPushButton[flat="true"]{ }     /* by Qt property */
```

## Pseudo-states (style ALL of these)

```css
QPushButton:hover     { background: #1d4ed8; }
QPushButton:pressed   { background: #1e40af; }
QPushButton:focus     { border: 2px solid #93c5fd; }   /* keep focus visible */
QPushButton:disabled  { color: #9ca3af; background: #e5e7eb; }
QCheckBox:checked     { }
QTabBar::tab:selected { }
```

## Sub-controls (`::`) — needed for complex widgets

```css
QComboBox::drop-down            { width: 20px; }
QComboBox QAbstractItemView     { background: #fff; selection-background-color: #2563eb; }
QScrollBar:vertical             { width: 12px; background: transparent; }
QScrollBar::handle:vertical     { background: #9ca3af; border-radius: 6px; min-height: 24px; }
QHeaderView::section            { background: #f1f5f9; padding: 6px; border: none; }
QCheckBox::indicator            { width: 16px; height: 16px; }
QCheckBox::indicator:checked    { image: url(:/icons/check.svg); }
```

## Box model gotchas (vs web CSS)
- `box-shadow` is **not supported** → use `QGraphicsDropShadowEffect` in code.
- `height` is often ignored on buttons; use `min-height` / `padding`.
- `margin` works on the widget's outer box; spacing between widgets is better
  done with **layout spacing**, not QSS margins.
- Gradients: `qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #..., stop:1 #...)`.
- Images/icons must come from the **resource system**: `url(:/icons/x.svg)`.

## Dark theme = QSS **and** QPalette

QSS alone leaves some native bits light (and you get a white flash on startup).
Set a dark `QPalette` too, before `show()`:

```python
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

def dark_palette() -> QPalette:
    p = QPalette()
    p.setColor(QPalette.Window, QColor("#1e1e1e"))
    p.setColor(QPalette.WindowText, QColor("#e5e7eb"))
    p.setColor(QPalette.Base, QColor("#252526"))
    p.setColor(QPalette.Text, QColor("#e5e7eb"))
    p.setColor(QPalette.Button, QColor("#2d2d30"))
    p.setColor(QPalette.ButtonText, QColor("#e5e7eb"))
    p.setColor(QPalette.Highlight, QColor("#2563eb"))
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor("#6b7280"))
    return p

app.setStyle("Fusion")            # Fusion respects QPalette well
app.setPalette(dark_palette())
app.setStyleSheet(THEME_QSS)      # then your stylesheet
```

## Token-driven QSS (one source of truth)

```python
TOKENS = {"accent": "#2563eb", "surface": "#252526", "text": "#e5e7eb",
          "border": "#3c3c3c", "radius": "6px"}

THEME_QSS = """
QWidget {{ background: {surface}; color: {text}; }}
QPushButton {{ background: {accent}; color: #fff; border-radius: {radius};
               padding: 6px 14px; min-height: 32px; }}
QPushButton:hover {{ background: #1d4ed8; }}
QPushButton:disabled {{ background: {border}; color: #9ca3af; }}
QLineEdit {{ border: 1px solid {border}; border-radius: {radius}; padding: 6px 10px; }}
QLineEdit:focus {{ border-color: {accent}; }}
""".format(**TOKENS)
```

## Common recipes
- **Card with elevation:** style a `QFrame` (radius + border) + apply
  `QGraphicsDropShadowEffect(blurRadius=16, xOffset=0, yOffset=2)`.
- **Zebra table:** `view.setAlternatingRowColors(True)` +
  `QTableView { alternate-background-color: #f8fafc; }`.
- **Primary vs secondary button:** `QPushButton#primary { background:{accent} }`
  vs `QPushButton[flat="true"] { background:transparent; color:{accent} }`.
