import QtQuick.Controls.Material

/*
    Simulation Configuration and Control
        Simulation Loader
        Source Map
        Controls

    Simulation Viewer
        Source Characteristics
        MPPT Characteristics
        MPPT VREF Over PV I-V, P-V Curve Cross-section
        System Efficiency
*/

Pane {
    Material.background: Material.Indigo

    PVSimulatorControls {
        id: pv_sim_controls
        width: parent.width * 1/4
    }

    PVSimulatorViewer {
        id: pv_sim_viewer
    }
}
