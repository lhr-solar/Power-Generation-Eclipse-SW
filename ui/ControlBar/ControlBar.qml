import QtQuick
import QtQuick.Controls

TabBar {
    anchors {
        left: parent.left
        right: parent.right
        top: parent.top
    }
    height: parent.height / 15
    contentHeight: parent.height / 15
    width: parent.width

    TabButton {
        text: "About"
    }

    TabButton {
        text: "PV Capture"
    }

    TabButton {
        text: "PV Designer"
    }

    TabButton {
        text: "PV Simulator"
    }
}
