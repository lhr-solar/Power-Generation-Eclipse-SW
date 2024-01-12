import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Pane {
    Material.background: Material.Green
    id: designer_page
    
    signal writeToConsole(string msg)
    signal sendToConfig(string cellID, double v_oc, double i_sc, double ref_temp, double ref_irrad, double ideality_factor)

    signal addNewCell(string cellID, string color, double v_oc, double i_sc, double ref_temp, double ref_irrad, double ideality_factor)
    signal modifyCell(string cellID, string color, double v_oc, double i_sc, double ref_temp, double ref_irrad, double ideality_factor)
    signal deleteCell(string cellID)
    signal saveConfig(string fileName)
    signal loadConfig(string fileName)


    function receiverSwitch(receiverID, msg) {
        switch(receiverID) {
            case 0: // console
                console.log(msg)
                writeToConsole(msg)
                break
            case 1: // add new cell
                console.log("receiverSwitch: add new cell")
                addNewCell(msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
                break
            case 2: // modify cell
                console.log("receiverSwitch: modify cell")
                console.log(msg)
                modifyCell(msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
                break
            case 3: // delete cell
                console.log("receiverSwitch: delete cell")
                deleteCell(msg)
                break
            case 4: // send cell data to console
                console.log("receiverSwitch: send cell data to config  " + msg)
                sendToConfig(msg[0], msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
                break
            case 5:
                console.log("save config")
                saveConfig(msg)
                break
            case 6:
                console.log("load config")
                loadConfig(msg)
                break
            default:
                console.log("receiverSwitch: receiverID not found")
                writeToConsole("receiverSwitch: receiverID not found")
        }
    }

    PVDesignerControls {
        id: pv_designer_controls
        width: parent.width * 1/4
        onWriteToParent: {
            receiverSwitch(receiverID, msg)
        }
        // TODO: figure out how to make this work so i dont get stupid deprecated function warnings
        // function onWriteToParent(receiverID, msg) {
        //     receiverSwitch(receiverID, msg)
        // }
    }


    PVDesignerViewer {
        id: pv_designer_viewer
        onWriteToParent: {
            receiverSwitch(receiverID, msg)
        }
    }
    // Layout.fillWidth: true
    // Layout.fillHeight: true
}
