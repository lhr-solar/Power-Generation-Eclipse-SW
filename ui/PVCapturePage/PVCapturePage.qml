import QtQuick.Controls.Material

/*
    Capture Configuration and Control
        Configuration
        Controls and Analysis
        CLI Terminal

    Characterization Viewer
        Source Characteristics
        I-V, P-V Curves
*/

Pane {
    Material.background: Material.BlueGrey

    PVCaptureControls {
        id: pv_cap_controls
        width: parent.width * 1/3
    }

    PVCaptureViewer {
        id: pv_cap_viewer
    }
}
