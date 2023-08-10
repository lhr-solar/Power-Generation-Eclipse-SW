import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true

    Rectangle {
        id: about_text
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
        }
        width: parent.width * 1/3
        color: "white"

        anchors.leftMargin: 20
        anchors.topMargin: 20

        ScrollView {
            anchors.fill: parent
            anchors.rightMargin: 20

            TextArea {
                objectName: "about_text"
                color: "black"
                Layout.preferredWidth: parent.width
                focus: true
                wrapMode: Text.WordWrap
                textFormat: TextEdit.MarkdownText
                placeholderText: "Loading about.md..."
            }
        }
    }

    Rectangle {
        id: about_image
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: about_text.right
            right: parent.right
        }
        color: "cornflowerblue"

        Image {
            id: texsun_image
            source: "../assets/texsun.jpg"

            autoTransform: true
            width: parent.width
            height: parent.height
            fillMode: Image.PreserveAspectCrop
        }
    }
}
