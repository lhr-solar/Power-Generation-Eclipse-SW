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
        startX: parent.width * 1.00
        startY: parent.height * 0.5
        PathLine { relativeX:-parent.width * 1.00 ; relativeY: parent.height * 0.00 }
        PathLine { relativeX: parent.width * 0.30 ; relativeY:-parent.height * 0.15 }
        PathLine { relativeX:-parent.width * 0.30 ; relativeY: parent.height * 0.15 }
        PathLine { relativeX: parent.width * 0.30 ; relativeY: parent.height * 0.15 }
    }
}
