import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: pv_designer_controls.right
        right: parent.right
    }
    anchors.margins: 15
    
    ListModel {
        id: pv_cell_list

        ListElement {
            name: "PV Cell 1"
            vmp: 0.5
            imp: 0.5
            voc: 0.6
            isc: 0.6
            pmp: 0.25
            color: "blue"
            x: 5
            y: 5
        }

        ListElement {
            name: "PV Cell 2"
            vmp: 0.5
            imp: 0.5
            voc: 0.6
            isc: 0.6
            pmp: 0.25
            color: "yellow"
            x: 5
            y: 7
        }
    }

    function addCell(name) {
        pv_cell_list.append({name: name})
    }

    GridView {
        anchors.fill: parent
        id: sim_view
        cellWidth: 10
        cellHeight: 10
        width: parent.right-parent.left
        height: parent.bottom-parent.top
        model: pv_cell_list
        snapMode: GridView.SnapToRow
        delegate: Rectangle {
            width: sim_view.cellWidth
            height: sim_view.cellHeight
            color: model.color
            // x: model.x
            // y: model.y

            property int snappedX: sim_view.cellWidth * Math.round(x / sim_view.cellWidth)
            property int snappedY: sim_view.cellHeight * Math.round(y / sim_view.cellHeight)

            x: snappedX
            y: snappedY

            MouseArea {
                id: sim
                anchors.fill: parent
                drag.target: parent

                onClicked: {
                    console.log("Clicked on " + model.text);
                    // Add your custom interaction logic here
                }

                onReleased: {
                    // Update the square's position when released
                    pv_cell_list.setProperty(index, "x", parent.snappedX);
                    pv_cell_list.setProperty(index, "y", parent.snappedY);
                }
            }
        }
    }
}
