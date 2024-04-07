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

                    ValueAxis {
                        id: xAxis
                        min: 0
                        max: 1
                    }

                    ValueAxis {
                        id: yAxis
                        min: 0
                        max: 1
                    }

                    ScatterSeries {
                        id: scatter1 
                        name: "AAA"
                        axisX: xAxis
                        axisY: yAxis
                    }

                    Connections {
                        target: plotSignals

                        function onSig_res(dataList) {
                            scatter1.append(dataList[1], dataList[2]);
                        }

                        // function onNew_point(point) {
                        //     scatter1.append(point.x, point.y);
                        // }

                        // function onRe_scale(maxy, miny, maxx, minx) {
                        //     xAxis.min = minx;
                        //     xAxis.max = maxx;
                        //     yAxis.min = miny;
                        //     yAxis.max = maxy;
                        // }
                    }

                    // ScatterSeries {
                    //     name: "AAA"

                    //     XYPoint { x: 1.5; y: 1.5 }
                    //     XYPoint { x: 1.5; y: 1.6 }
                    //     XYPoint { x: 1.57; y: 1.55 }
                    //     XYPoint { x: 1.8; y: 1.8 }
                    //     XYPoint { x: 1.9; y: 1.6 }
                    //     XYPoint { x: 2.1; y: 1.3 }
                    //     XYPoint { x: 2.5; y: 2.1 }
                    // }
                }
            }
        }
    }
}
