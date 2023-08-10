import QtQuick
import QtQuick.Shapes

Shape {
    anchors {
        centerIn: parent
        topMargin: parent.height * 0.1
        bottomMargin: parent.height * 0.1
        leftMargin: parent.width * 0.1
        rightMargin: parent.width * 0.1
    }

    height: parent.height * 0.8
    width: parent.width * 0.8

    ShapePath {
        strokeWidth: 3
        strokeColor: "black"
        capStyle: ShapePath.RoundCap

        property int joinStyleIndex: 2

        property variant styles: [
            ShapePath.BevelJoin,
            ShapePath.MiterJoin,
            ShapePath.RoundJoin
        ]

        joinStyle: styles[joinStyleIndex]

        scale: "0.8x0.8"
        startX: parent.width * 0.50
        startY: parent.height * 1.0
        PathLine { relativeX: parent.width * 0.00 ; relativeY:-parent.height * 1.00 }
        PathLine { relativeX:-parent.width * 0.15 ; relativeY: parent.height * 0.30 }
        PathLine { relativeX: parent.width * 0.15 ; relativeY:-parent.height * 0.30 }
        PathLine { relativeX: parent.width * 0.15 ; relativeY: parent.height * 0.30 }
    }
}
