// devcycle-ui — generated QML token singleton.
// Mirrors the SAME semantic tokens as theme.qss so QML and QWidget layers share
// one design system (QSS does not cascade into QML — keep them in sync here).
// Register with: qmlRegisterSingletonType or a `pragma Singleton` + qmldir.
pragma Singleton
import QtQuick

QtObject {
    // tokens (dark example — keep in lockstep with theme.qss)
    readonly property color accent:      "#4f8cff"
    readonly property color surface:     "#1e1f22"
    readonly property color surfaceAlt:  "#26282c"
    readonly property color text:        "#e6e6e6"
    readonly property color textMuted:   "#9aa0a6"
    readonly property color border:      "#34373b"
    readonly property color danger:      "#e5484d"

    readonly property int radius:   6
    readonly property int spacing:  8
    readonly property int fontPt:   10
}
