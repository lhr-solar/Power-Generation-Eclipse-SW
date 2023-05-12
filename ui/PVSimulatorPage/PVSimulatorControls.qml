import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import Qt.labs.qmlmodels

import "../Arrows"

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

            GridLayout {
                anchors {
                    fill: parent
                    topMargin: parent.height * 0.1
                    bottomMargin: parent.height * 0.1
                    leftMargin: parent.width * 0.1
                    rightMargin: parent.width * 0.1
                }

                columns: 3
                columnSpacing: 0
                rowSpacing: 0

                Repeater {
                    model: ListModel {
                        ListElement {
                            type: "button"
                            name: "Environment"
                            color: "#FF5722"
                            row: 0
                            col: 0
                            span: 1
                        }
                        ListElement {
                            type: "button"
                            name: "Photovoltaic"
                            color: "#FFC107"
                            row: 0
                            col: 2
                            span: 1
                        }
                        ListElement {
                            type: "button"
                            name: "MPPT"
                            color: "#8BC34A"
                            row: 2
                            col: 2
                            span: 1
                        }
                        ListElement {
                            type: "button"
                            name: "MPPT\nAlgorithm"
                            color: "#03A9F4"
                            row: 4
                            col: 0
                            span: 3
                        }
                        ListElement {
                            type: "button"
                            name: "Load"
                            color: "#3F51B5"
                            row: 2
                            col: 0
                            span: 1
                        }
                        ListElement {
                            type: "arrow_right"
                            name: "arrow_1"
                            color: "black"
                            row: 0
                            col: 1
                            span: 1
                        }
                        ListElement {
                            type: "arrow_down"
                            name: "arrow_2"
                            color: "black"
                            row: 1
                            col: 2
                            span: 1
                        }
                        ListElement {
                            type: "arrow_downleft"
                            name: "arrow_3"
                            color: "black"
                            row: 3
                            col: 2
                            span: 1
                        }
                        ListElement {
                            type: "arrow_upleft"
                            name: "arrow_4"
                            color: "black"
                            row: 3
                            col: 0
                            span: 1
                        }
                    }

                    delegate: DelegateChooser {
                        role: "type"
                        DelegateChoice {
                            roleValue: "button"
                            delegate:
                                Button {
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredHeight: parent.height * 0.25
                                    Layout.preferredWidth: parent.width   * 0.45
                                    Layout.column: model.col
                                    Layout.row: model.row
                                    Layout.columnSpan: model.span

                                    background: Rectangle {
                                        anchors.fill: parent
                                        color: parent.down ? "#607D8B": model.color
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

                                    text: model.name
                                }
                        }

                        DelegateChoice {
                            roleValue: "arrow_right"
                            delegate:
                                Rectangle {
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredHeight: parent.height * 0.125
                                    Layout.preferredWidth: parent.width   * 0.100
                                    Layout.column: model.col
                                    Layout.row: model.row
                                    Layout.columnSpan: model.span

                                    ArrowRight {}
                                }
                        }

                        DelegateChoice {
                            roleValue: "arrow_down"
                            delegate:
                                Rectangle {
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredHeight: parent.height * 0.125
                                    Layout.preferredWidth: parent.width   * 0.125
                                    Layout.column: model.col
                                    Layout.row: model.row
                                    Layout.columnSpan: model.span

                                    ArrowDown {}
                                }
                        }

                        DelegateChoice {
                            roleValue: "arrow_downleft"
                            delegate:
                                Rectangle {
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredHeight: parent.height * 0.125
                                    Layout.preferredWidth: parent.width   * 0.125
                                    Layout.column: model.col
                                    Layout.row: model.row
                                    Layout.columnSpan: model.span

                                    ArrowDownLeft {}
                                }
                        }

                        DelegateChoice {
                            roleValue: "arrow_upleft"
                            delegate:
                                Rectangle {
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredHeight: parent.height * 0.125
                                    Layout.preferredWidth: parent.width   * 0.125
                                    Layout.column: model.col
                                    Layout.row: model.row
                                    Layout.columnSpan: model.span

                                    ArrowUpLeft {}
                                }
                        }
                    }
                }
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
