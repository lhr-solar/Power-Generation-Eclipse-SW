import QtQuick.Controls.Material


Pane {
    Material.background: Material.Red

    PVCharacteristicsControls {
        id: pv_char_controls
        width: parent.width * 1/4
    }

    PVCharacteristicsViewer {
        id: pv_char_viewer
    }
}
