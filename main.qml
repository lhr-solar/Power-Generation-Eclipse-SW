import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls.Material

import "ui/AboutPage"
import "ui/ControlBar"
import "ui/PVCapturePage"
import "ui/PVDesignerPage"
import "ui/PVSimulatorPage"

Window {
    width: 1920
    height: 1080
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Purple

    title: qsTr("Eclipse")

    ControlBar {
        id: control_bar
        objectName: "control_bar"
    }

    Rectangle {
        anchors {
            top: control_bar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        objectName: "main_view"

        StackLayout {
            id: main_layout
            currentIndex: control_bar.currentIndex
            anchors.fill: parent

            // About page
            AboutPage {
                id: about_page
            }

            // Control I-V Curve Tracer
            PVCapturePage {
                id: pv_capture
            }

            // Design PV array
            PVDesignerPage {
                id: pv_designer
            }

            // Simulate PV array and MPPT
            PVSimulatorPage {
                id: pv_simulator
            }
        }
    }
}
