import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import "ui/AboutPage"
import "ui/ControlBar"

Window {
    width: 1080
    height: 720
    visible: true
    title: qsTr("Eclipse")

    ControlBar {
        id: control_bar
    }

    Rectangle {
        anchors {
            top: control_bar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        StackLayout {
            id: main_layout
            currentIndex: control_bar.currentIndex
            anchors.fill: parent

            // About page
            AboutPage {
                id: about_page
            }

            // Control I-V Curve Tracer
            Rectangle {
                id: pv_capture
                color: 'plum'
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            // Design PV array
            Rectangle {
                id: pv_designer
                color: 'teal'
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            // Simulate PV array and MPPT
            Rectangle {
                id: pv_simulator
                color: 'goldenrod'
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }
}
