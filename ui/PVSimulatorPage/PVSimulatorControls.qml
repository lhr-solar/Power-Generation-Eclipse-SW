import QtQuick
import QtQuick.Layouts

/*
    Simulation Configuration and Control
        Simulation Loader
        Source Map
        Controls
*/

Rectangle {
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: parent.left
    }
    anchors.margins: 15

    GridLayout {
        anchors.fill: parent
        columns: 1
        rowSpacing: 0

        Rectangle {
            Layout.minimumHeight: parent.height * 0.4
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            Text {
                text: "Simulation Loader"
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.4
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            Text {
                text: "Source Map"
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.2
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            Text {
                text: "Controls"
                anchors.centerIn: parent
            }
        }
    }
}
