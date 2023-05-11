import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts

Rectangle {
    color: 'plum'
    Layout.fillWidth: true
    Layout.fillHeight: true

    Rectangle {
        id: pv_capture_control_console
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
        }
        width: parent.width * 1/3
//        color: "lightgreen"

        GridLayout {
            anchors.fill: parent
            anchors.margins: 15
            columns: 1

            Text {
                text: "Configuration"
                font.pointSize: 15
                Layout.alignment: Qt.AlignHCenter
                color: "black"
            }

            Rectangle {
                Layout.minimumHeight: parent.height * 0.3
                Layout.minimumWidth: parent.width
                border {
                    width: 1
                }

                Text {
                    text: "Config Box"
                    anchors.centerIn: parent
                }
            }

            Text {
                text: "Controls and Analysis"
                font.pointSize: 15
                Layout.alignment: Qt.AlignHCenter
                color: "black"
            }

            Rectangle {
                Layout.minimumHeight: parent.height * 0.3
                Layout.minimumWidth: parent.width
                border {
                    width: 1
                }

                Text {
                    text: "Controls Box"
                    anchors.centerIn: parent
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

    Rectangle {
        id: pv_capture_view
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: pv_capture_control_console.right
            right: parent.right
        }
//        color: "lavender"

        GridLayout {
            columns: 2
            anchors.fill: parent
            anchors.margins: 15

            Text {
                text: "Characterization"
                font.pointSize: 15
                Layout.columnSpan: 2
                Layout.alignment: Qt.AlignHCenter
                color: "black"
            }

            Repeater {
                model: [
                    { title: "V<sub>OC</sub> (V)" , ref: "v_oc"  },
                    { title: "I<sub>SC</sub> (A)" , ref: "i_sc"  },
                    { title: "FF (%)"             , ref: "ff"    },
                    { title: "V<sub>MPP</sub> (V)", ref: "v_mpp" },
                    { title: "I<sub>MPP</sub> (A)", ref: "i_mpp" },
                    { title: "P<sub>MPP</sub> (W)", ref: "p_mpp" }
                ]
                Rectangle {
                    Layout.minimumHeight: parent.height * 0.03
                    Layout.minimumWidth: parent.width * 0.485
                    Layout.alignment: Qt.AlignHCenter
                    GridLayout {
                        anchors.centerIn: parent
                        columns: 2

                        Label {
                            Layout.alignment: Qt.AlignRight
                            color: "black"
                            textFormat: Text.RichText
                            text: modelData.title
                        }

                        TextArea {
                            font.bold: true
                            color: "blue"
                            placeholderText: "N/A"
                            objectName: modelData.ref
                            readOnly: true
                        }
                    }
                }
            }

            ChartView {
                title: "PV Curves"
                Layout.minimumHeight: parent.height * 0.85
                Layout.minimumWidth: parent.width
                Layout.columnSpan: 2
                theme: ChartView.ChartThemeQt
                antialiasing: true

                ScatterSeries {
                    id: iv_curve
                    name: "I-V Curve"
                    XYPoint { x: 1.5; y: 1.5 }
                    XYPoint { x: 1.5; y: 1.6 }
                    XYPoint { x: 1.57; y: 1.55 }
                    XYPoint { x: 1.8; y: 1.8 }
                    XYPoint { x: 1.9; y: 1.6 }
                    XYPoint { x: 2.1; y: 1.3 }
                    XYPoint { x: 2.5; y: 2.1 }
                }

                ScatterSeries {
                    id: pv_curve
                    name: "P-V Curve"
                    XYPoint { x: 2.0; y: 2.0 }
                    XYPoint { x: 2.0; y: 2.1 }
                    XYPoint { x: 2.07; y: 2.05 }
                    XYPoint { x: 2.2; y: 2.9 }
                    XYPoint { x: 2.4; y: 2.7 }
                    XYPoint { x: 2.67; y: 2.65 }
                }
            }
        }
    }
}
