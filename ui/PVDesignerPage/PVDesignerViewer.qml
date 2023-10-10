import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import "../Cell"

Rectangle {
    id: pv_designer_view_rect
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: pv_designer_controls.right
        right: parent.right
    }
    anchors.margins: 15
    
    signal writeToParent(int receiverID, var msg)

    Connections {
        target: designer_page
        onAddNewCell: {
            // addCell(cellID, color, v_oc, i_sc, ref_temp, ref_irrad, ideality_factor)
            joemama(cellID, color, 1, 1)
        }
    }

    ListModel {
        id: pv_cell_list

        ListElement {
            name: "PV Cell 1"
            color: "blue"
            x: 0
            y: 0
        }
        // Cell {
        //     name: "PV Cell 1"
        //     color: "blue"
        //     x: 0
        //     y: 0
        //     ref_v_oc: 1
        //     ref_i_sc: 1
        //     ref_irrad: 1
        //     ref_temp: 1
        //     ref_ideality: 1
        // }

        // Cell {
        //     name: "PV Cell 2"
        //     color: "yellow"
        //     x: 4
        //     y: 10
        //     ref_v_oc: 1
        //     ref_i_sc: 1
        //     ref_irrad: 1
        //     ref_temp: 1
        //     ref_ideality: 1
        // }
    }

    function joemama(name1, color1, x1, y1){
        pv_cell_list.append({name: name1,
            color: color1, 
            x: x1,
            y: y1
            })
    }

    // function addCell(cellID, cellColor, voc, i_sc, temp, irrad, ideality) {
    //     var object newObject = Qt.createQmlObject(`
    //     import "../Cell"

    //     Cell {
    //         name: "` + name1 + `"
    //         color: "` + color1 + `"
    //         x: 1
    //         y: 1
    //         ref_v_oc: ` + voc + `
    //         ref_i_sc: ` + i_sc + `
    //         ref_irrad: ` + irrad + `
    //         ref_temp: ` + temp + `
    //         ref_ideality: ` + ideality + `
    //     }
    //     `,
    //     pv_cell_list,
    //     "PVDesignerViewer"
    //     );
    //     var object = Qt.createQmlObject( "import QtQuick; Cell { name: '" + name1 + "'; color: '" + color1 + "'; ref_v_oc: " + voc + "; ref_i_sc: " + i_sc + "; ref_irrad: " + irrad + "; ref_temp: " + temp + "; ref_ideality: " + ideality + "}", pv_cell_list)
    // }

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
                

                //parent.parent.parent.parent.parent.parent.

                //TODO: send cell data to module viewer in design control
                onClicked: {
                    writeToParent(4, [parent.name, parent.color, parent.ref_v_oc, parent.ref_i_sc, parent.ref_temp, parent.ref_irrad, parent.ref_ideality])
                }

                onReleased: {
                    // console.log("x: " + parent.x + " y: " + parent.y)
                    parent.x = snappedX(parent.x)
                    parent.y = snappedY(parent.y)
                }
            }
        }
    }
}
