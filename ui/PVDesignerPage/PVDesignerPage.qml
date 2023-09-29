import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Pane {
    Material.background: Material.Green
    id: designer_page
    
    signal writeToConsole(string msg)

    function receiverSwitch(receiverID, msg) {
        switch(receiverID) {
            case 0: // console
                console.log(msg)
                writeToConsole(msg)
                break
            default:
                console.log("receiverSwitch: receiverID not found")
                writeToConsole("receiverSwitch: receiverID not found")
        }
    }

    PVDesignerControls {
        id: pv_designer_controls
        width: parent.width * 1/4
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
