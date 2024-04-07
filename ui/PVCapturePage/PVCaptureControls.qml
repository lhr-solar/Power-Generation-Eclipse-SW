import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

/*
    Capture Configuration and Control
        Configuration
        Controls and Analysis
        CLI Terminal
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
            Layout.minimumHeight: parent.height * 0.3
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            Text {
                text: "Configuration"
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
                text: "Controls and Analysis"
                anchors.centerIn: parent

                visible: false
            }

            Button {
                id: plotButton
                text: "Plot"
                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    plotSignals.plot()
                }
            }
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.3
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            color: "black"
            ScrollView {
                anchors.fill: parent

                TextArea {
                    objectName: "console"
                    color: "white"
                    Layout.preferredWidth: parent.width
                    focus: true
                    wrapMode: Text.WordWrap
                    placeholderText: "TYPE COMMAND then CTRL+ENTER to use CLI."

                    Keys.onReturnPressed: (event) => {
                        if(event.modifiers & Qt.ControlModifier) {
                            text += '\n'
                            cursorPosition = text.length
                            // TODO: update backend
                            console.log("hi!")
                        }
                    }
                }
            }
        }
    }
}
