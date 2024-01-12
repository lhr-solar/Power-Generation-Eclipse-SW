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
    
    signal writeToParent(int receiverID, var msg)

    Connections {
        target: designer_page
        onAddNewCell: {
            addCell(cellID, color, v_oc, i_sc, ref_temp, ref_irrad, ideality_factor)
            // joemama(cellID, color, 1, 1)
        }
        onModifyCell: {
            modifyCell(cellID, color, v_oc, i_sc, ref_temp, ref_irrad, ideality_factor)
        }
        onDeleteCell: {
            deleteCell(cellID)
        }
        onSaveConfig: {
            console.log("saving config")
            var filePath = fileName + ".array_conf"
        }
        onLoadConfig: {
            console.log("loading config")
            var filePath = fileName + ".array_conf"
        }
    }

    ListModel {
        id: pv_cell_list
    }

    function addCell(cellID, cellColor, v_oc, i_sc, temp, irrad, ideality) {
        pv_cell_list.append({name: cellID,
            color: cellColor, 
            ref_v_oc: v_oc,
            ref_i_sc: i_sc,
            ref_temp: temp,
            ref_irrad: irrad,
            ideality_factor: ideality,
            x: 0,
            y: 0
            })
    }

    function modifyCell(cellID, cellColor, v_oc, i_sc, temp, irrad, ideality) {
        console.log("bazinga")
        for(var i = 0; i < pv_cell_list.count; i++) {
            console.log("cellID: " + cellID)
            console.log("pv_cell_list.get(i).name: " + pv_cell_list.get(i).name)
            if(pv_cell_list.get(i).name == cellID) {
                var X = pv_cell_list.get(i).x
                var Y = pv_cell_list.get(i).y
                console.log("x: " + X + " y: " + Y)
                pv_cell_list.set(i, {name: cellID,
                    color: cellColor, 
                    ref_v_oc: v_oc,
                    ref_i_sc: i_sc,
                    ref_temp: temp,
                    ref_irrad: irrad,
                    ideality_factor: ideality,
                    x: X,
                    y: Y
                    })
                break
            }
        }
    }

    function deleteCell(cellID) {
        for(var i = 0; i < pv_cell_list.count; i++) {
            if(pv_cell_list.get(i).name == cellID) {
                pv_cell_list.remove(i)
                break
            }
        }
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
            
            objectName: "summaryDelegate"
            property int index: model.index

            property string name: model.name
            property double v_oc: model.ref_v_oc
            property double i_sc: model.ref_i_sc
            property double temp: model.ref_temp
            property double irrad: model.ref_irrad
            property double ideality: model.ideality_factor
            
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
                // console.log("current y: " + current_y)
                if(current_y < 0) {
                    return 0
                } 
                if (current_y > sim_view.height) {
                    return sim_view.height-height
                }
                return Math.round(current_y/sim_view.cellHeight)*sim_view.cellHeight
            }

            function loadCoords() { //set x/y to positions in model
                x = model.x*width
                y = model.y*height
                console.log("x: " + model.x*width + " y: " + model.y*height)
                console.log("x: " + x + " y: " + y)
            }

            function saveCoords() { //set model x/y to positions
                model.x = x/width
                model.y = y/height
            }
            
            MouseArea {
                id: sim_drag
                anchors.fill: parent
                drag.target: parent
                

                //parent.parent.parent.parent.parent.parent.

                //TODO: send cell data to module viewer in design control
                onClicked: {
                    writeToParent(4, [parent.name, parent.v_oc, parent.i_sc, parent.temp, parent.irrad, parent.ideality])
                    // initializeView()
                }

                onReleased: {
                    // console.log("x: " + parent.x + " y: " + parent.y)
                    parent.x = snappedX(parent.x)
                    // model.x = parent.x/parent.width
                    parent.y = snappedY(parent.y)
                    // model.y = parent.y/parent.height
                }
            }
        }

        // Code below courtesy of: @chazomaticus at https://stackoverflow.com/questions/9039497/how-to-get-an-instantiated-delegate-component-from-a-gridview-or-listview-in-qml
        // Uses black magic to hunt for the delegate instance with the given
        // index.  Returns undefined if there's no currently instantiated
        // delegate with that index.
        function getDelegateInstanceAt(index) {
            for(var i = 0; i < contentItem.children.length; ++i) {
                var item = contentItem.children[i];
                // We have to check for the specific objectName we gave our
                // delegates above, since we also get some items that are not
                // our delegates here.
                if (item.objectName == "summaryDelegate" && item.index == index)
                    return item;
            }
            return undefined;
        }
        // End stolen code
    }

    GridLayout {
        id: coord_buttons
        anchors {
            bottom: parent.bottom
            right: parent.right
        }
        columns: 1
        rows: 2
        width: 200
        height: 100
        Button {
            id: save_coords
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Save Array Coords"
            onClicked: {
                for(var i = 0; i < pv_cell_list.count; i++) {
                    var item = sim_view.getDelegateInstanceAt(i)
                    if(item != undefined) {
                        item.saveCoords()
                    }
                }
            }
        }
        Button {
            id: load_coords
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Load Array Coords"
            onClicked: {
                for(var i = 0; i < pv_cell_list.count; i++) {
                    var item = sim_view.getDelegateInstanceAt(i)
                    if(item != undefined) {
                        item.loadCoords()
                    }
                }
            }
        }
    }
}
