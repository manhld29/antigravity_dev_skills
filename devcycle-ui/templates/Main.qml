// devcycle-ui — generated QML view starter (Quick Controls 2).
// Self-styled from Theme.qml tokens. Set the Quick Controls style in Python
// BEFORE loading (QQuickStyle.setStyle("Material")), or via render_ui.py
// --quick-style Material. Wire a backend QObject as a context property for logic.
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
// import "." as App   // when Theme.qml singleton is registered via qmldir

Rectangle {
    id: root
    anchors.fill: parent
    color: "#1e1f22"          // = Theme.surface (token)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 8

        Label {
            text: "QML view preview"
            color: "#e6e6e6"
            font.pointSize: 14
            font.bold: true
        }

        TextField {
            Layout.fillWidth: true
            placeholderText: "Text input"
        }

        ComboBox {
            Layout.fillWidth: true
            model: ["Option A", "Option B", "Option C"]
        }

        RowLayout {
            spacing: 8
            Button {
                text: "Primary"
                highlighted: true
                Accessible.name: "Primary action"
            }
            Button { text: "Secondary" }
            Button { text: "Disabled"; enabled: false }
        }

        ProgressBar {
            Layout.fillWidth: true
            value: 0.6
        }

        Item { Layout.fillHeight: true }   // push content to the top
    }
}
