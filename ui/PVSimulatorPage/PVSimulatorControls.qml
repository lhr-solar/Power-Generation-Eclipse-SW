import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

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

        PVSimulatorConfig {
            Layout.minimumHeight: parent.height * 0.4
            Layout.minimumWidth: parent.width
        }

        PVSimulatorSourceMap {
            Layout.minimumHeight: parent.height * 0.45
            Layout.minimumWidth: parent.width
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.15
            Layout.minimumWidth: parent.width

            GridLayout {
                anchors.fill: parent
                anchors.margins: 15
                columns: 4
                columnSpacing: 0
                rowSpacing: 0

                Text {
                    Layout.preferredHeight: parent.height * 0.2
                    Layout.preferredWidth: parent.width
                    Layout.column: 0
                    Layout.row: 0
                    Layout.columnSpan: 4
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: "Simulation Cycle"
                }

                Label {
                    Layout.preferredHeight: parent.height * 0.4
                    Layout.preferredWidth: parent.width   * 0.1
                    Layout.row: 1
                    Layout.column: 0
                    Layout.columnSpan: 1

                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: "black"
                    text: "N/A"
                }

                Slider {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.preferredHeight: parent.height * 0.4
                    Layout.preferredWidth: parent.width   * 0.8
                    Layout.row: 1
                    Layout.column: 1
                    Layout.columnSpan: 2

                    from: 1
                    value: 25
                    to: 100
                }

                Label {
                    Layout.alignment: Qt.AlignHCenter
                    Layout.preferredHeight: parent.height * 0.4
                    Layout.preferredWidth: parent.width   * 0.1
                    Layout.row: 1
                    Layout.column: 3
                    Layout.columnSpan: 1

                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: "black"
                    text: "N/A"
                }

                Button {
                    Layout.alignment: Qt.AlignLeft
                    Layout.preferredHeight: parent.height * 0.4
                    Layout.preferredWidth: parent.width   * 0.4
                    Layout.row: 2
                    Layout.column: 0
                    Layout.columnSpan: 2

                    background: Rectangle {
                        anchors.fill: parent
                        color: parent.down ? "#607D8B": "red"
                        radius: 0
                    }

                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        opacity: enabled ? 1.0 : 0.3
                        color: "black"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                        fontSizeMode: Text.Fit
                    }

                    text: "RESET"
                }

                Button {
                    Layout.alignment: Qt.AlignRight
                    Layout.preferredHeight: parent.height * 0.4
                    Layout.preferredWidth: parent.width   * 0.4
                    Layout.row: 2
                    Layout.column: 2
                    Layout.columnSpan: 2

                    background: Rectangle {
                        anchors.fill: parent
                        color: parent.down ? "#607D8B": "green"
                        radius: 0
                    }

                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        opacity: enabled ? 1.0 : 0.3
                        color: "black"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                        fontSizeMode: Text.Fit
                    }

                    text: "RUN"
                }
            }
        }
    }
}
