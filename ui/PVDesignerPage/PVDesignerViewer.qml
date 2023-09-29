import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: pv_designer_view_rect
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: pv_designer_controls.right
        right: parent.right
    }
    anchors.margins: 15
    
    signal writeToParent(int receiverID, string msg)

    ListModel {
        id: pv_cell_list

        ListElement {
            name: "PV Cell 1"
            color: "blue"
            x: 0
            y: 0
        }

        ListElement {
            name: "PV Cell 2"
            color: "yellow"
            x: 0
            y: 1
        }
    }

    function addCell(name1, color1, x1, y1) {
        pv_cell_list.append({name: name1,
            color: color1, 
            x: x1,
            y: y1
            })
    }

    GridView {
        anchors.fill: parent
        id: sim_view
        cellWidth: 20
        cellHeight: 20
        width: parent.right-parent.left
        height: parent.bottom-parent.top
        model: pv_cell_list
        // snapMode: GridView.SnapToRow
        boundsBehavior: Flickable.StopAtBounds

        
        // property string[][] cellGrid: [[]]
        
        

        delegate: Rectangle {
            width: sim_view.cellWidth
            height: sim_view.cellHeight
            color: model.color
            x: model.x*width
            y: model.y*height
            
            //Snaps to grid in x direction
            function snappedX(current_x) {
                if(current_x < 0) {
                    return 0
                } 
                if (current_x > sim_view.width) {
                    return sim_view.width-width
                }
                return Math.round(current_x/sim_view.cellWidth)*sim_view.cellWidth
            }
            //Snaps to grid in y direction
            function snappedY(current_y) {
                if(current_y < 0) {
                    return 0
                } 
                if (current_y > sim_view.height) {
                    return sim_view.height-height
                }
                return Math.round(current_y/sim_view.cellHeight)*sim_view.cellHeight
            }

            

            // Connections {
            //     target: parent

            //     function onWriteToConsole(msg) {
            //         console.log(msg)
            //     }
            // }

            
            
            MouseArea {
                id: sim_drag
                anchors.fill: parent
                drag.target: parent
                property int i: 2

                //parent.parent.parent.parent.parent.parent.

                // Currently just adds another cell, but will eventually add a menu to add cell with custom characteristics
                onClicked: {
                    addCell("PV Cell " + i, "red", i, i)
                    pv_designer_view_rect.writeToParent(0, "added cell")
                    i++
                }

                onReleased: {
                    console.log("x: " + parent.x + " y: " + parent.y)
                    parent.x = snappedX(parent.x)
                    parent.y = snappedY(parent.y)
                }
            }
        }
    }
}
