import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Pane {
    Material.background: Material.Green

    PVDesignerControls {
        id: pv_designer_controls
        width: parent.width * 1/4
    }

    PVDesignerViewer {
        id: pv_designer_viewer
    }
    // Layout.fillWidth: true
    // Layout.fillHeight: true
}
