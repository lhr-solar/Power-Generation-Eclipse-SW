import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true

    Rectangle {
        id: about_image
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
        }
        color: "cornflowerblue"
        width: parent.width * 2/3

        Image {
            id: texsun_image
            source: "../assets/texsun.jpg"

            autoTransform: true
            width: parent.width
            height: parent.height
            fillMode: Image.PreserveAspectCrop
        }
    }

    Rectangle {
        anchors {
            top: parent.top
            bottom: parent.bottom
            right: parent.right
            left: about_image.right
        }
        color: "white"

        anchors.leftMargin: 20
        anchors.topMargin: 20
        anchors.rightMargin: 20

        ScrollView {
            anchors.fill: parent
            TextArea {
                id: about_text
                color: "black"
                Layout.preferredWidth: parent.width
                focus: true
                wrapMode: Text.WordWrap
                textFormat: TextEdit.MarkdownText
                text:
"
# Eclipse

Eclipse is a multifunctional application to characterize UT Austin's LHR Solar power generation system.
It performs the following tasks:
- control and monitor the IV Curve Tracer,
- characterize and evaluate photovoltaic systems,
- create and model said systems,
- and simulate a virtual power generation system.

---
## What's New (Doc)

`Version 4.0.0`

TODO: this

---
## Credits

The main author of this revision is Matthew Yu (matthewjkyu@gmail.com).
The greater assistant author is Roy Mor.
The lesser assistant author is Jared McArthur.

Also credits to the following members of LHR Solar who have contributed
previously to MPPT algorithm components:
- Afnan Mir
- Gary Hallock

---
## Copyright


Copyright (C) 2023 by Matthew Yu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"
                }
        }
    }


}
