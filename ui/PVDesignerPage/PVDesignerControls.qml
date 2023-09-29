import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

/* TODO:
    * Add module creator
    * add module viewer/editor, same region as ^ but separate windows/dropdowns?
    * add file save/load capabilities for modules/cell designs
*/


Rectangle {
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: parent.left
    }
    anchors.margins: 15

    Connections {
        target: designer_page
        onWriteToConsole: {
            designer_console.text += msg + "\n"
        }
    }

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
            ComboBox {
                id: config_combo
                anchors.fill: parent
                model: ["First", "Second", "Third"]
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
                    id: designer_console
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
