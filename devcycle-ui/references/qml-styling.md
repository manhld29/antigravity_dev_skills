# QML styling (Qt Quick Controls 2)

Load when building QML UI. Quick Controls 2 ships swappable **styles** and two
themeable styles with an accent (`Material`, `Universal`).

## Choose the style once, at startup

```python
from PySide6.QtQuickControls2 import QQuickStyle
QQuickStyle.setStyle("Material")   # Basic | Fusion | Material | Universal | macOS | iOS
# then create QQmlApplicationEngine and load the QML
```
Or via env: `QT_QUICK_CONTROLS_STYLE=Material`. Don't import a concrete style
(`QtQuick.Controls.Material`) for controls you want themeable — import
`QtQuick.Controls` and let the style apply.

## Theme + accent (Material / Universal)

```qml
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ApplicationWindow {
    Material.theme: Material.Dark          // or Material.Light / Material.System
    Material.accent: "#2563eb"
    Material.primary: "#1e293b"
    Button { text: "Save"; highlighted: true }
}
```
`Universal` is the Fluent/Windows look: `Universal.theme`, `Universal.accent`.

## Centralize tokens in a singleton

`Theme.qml`:
```qml
pragma Singleton
import QtQuick
QtObject {
    readonly property color accent:  "#2563eb"
    readonly property color surface: "#1e1e1e"
    readonly property color text:    "#e5e7eb"
    readonly property int   radius:  8
    readonly property int   spacing: 8
}
```
Register it (`qmldir`: `singleton Theme Theme.qml`) then `Theme.accent` anywhere.
One source of truth → dark mode = swap the singleton's values.

## Layouts, not absolute positioning

```qml
import QtQuick.Layouts
ColumnLayout {
    anchors.fill: parent
    spacing: Theme.spacing
    TextField  { Layout.fillWidth: true; placeholderText: "Name" }
    Button     { Layout.alignment: Qt.AlignRight; text: "Submit" }
}
```
Never put `anchors.fill` on a child **inside** a Layout — set `Layout.*` hints.

## Custom-styled control (keep accessibility)

```qml
Button {
    id: ctl
    text: "Export"
    Accessible.role: Accessible.Button
    Accessible.name: text
    background: Rectangle {
        radius: Theme.radius
        color: ctl.pressed ? "#1e40af" : ctl.hovered ? "#1d4ed8" : Theme.accent
        Behavior on color { ColorAnimation { duration: 150 } }
    }
    contentItem: Text { text: ctl.text; color: "#fff"; horizontalAlignment: Text.AlignHCenter }
}
```

## Connect to Python

```python
backend = Backend()                      # a QObject with @Slot/@Signal/Property
engine.rootContext().setContextProperty("backend", backend)
# QML: Button { onClicked: backend.save(field.text) }
```

## Performance
- Keep property bindings cheap; compute in Python and expose a `Property`.
- Large lists: `ListView`/`TableView` with `reuseItems: true` — not `Repeater`.
- Animate `opacity`/`scale`/position via `Behavior`, 150–250ms; respect a
  reduced-motion setting you expose from the backend.

## High-DPI
QML uses logical pixels and scales automatically. Use implicit sizes + Layout
hints, and **SVG** icons (`Image { source: "qrc:/i/save.svg" }`).
