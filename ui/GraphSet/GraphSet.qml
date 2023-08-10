import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts

Rectangle {
    Layout.minimumHeight: parent.height * 0.5
    Layout.minimumWidth: parent.width * 0.5

    ComboBox {
        id: combo
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }

        textRole: "chart_title"
        model: parent.model

        contentItem: Text {
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            leftPadding: parent.width * 0.03
            textFormat: Text.RichText
            text: parent.displayText
            font: combo.font
            color: "black"
        }
    }

    Rectangle {
        anchors {
            top: combo.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }

        StackLayout {
            currentIndex: combo.currentIndex
            anchors.fill: parent

            Repeater {
                model: parent.parent.parent.model

                ChartView {
                    objectName: model.key
                    theme: ChartView.ChartThemeQt
                    antialiasing: true

                    ScatterSeries {
                        name: "AAA"
                        XYPoint { x: 1.5; y: 1.5 }
                        XYPoint { x: 1.5; y: 1.6 }
                        XYPoint { x: 1.57; y: 1.55 }
                        XYPoint { x: 1.8; y: 1.8 }
                        XYPoint { x: 1.9; y: 1.6 }
                        XYPoint { x: 2.1; y: 1.3 }
                        XYPoint { x: 2.5; y: 2.1 }
                    }
                }
            }
        }
    }
}
