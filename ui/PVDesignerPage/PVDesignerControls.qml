import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import "../MLDoubleSpinBox"

/* TODO:
    * Add module creator
    * add module viewer/editor, same region as ^ but separate windows/dropdowns?
    * add file save/load capabilities for modules/cell designs
*/


Rectangle {
    id: pv_designer_controls_rect
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: parent.left
    }
    // color: "green"
    anchors.margins: 15


    signal writeToParent(int receiverID, var msg)

    Connections {
        target: designer_page
        onWriteToConsole: {
            designer_console.text += msg + "\n"
        }
    }

    Connections {
        target: designer_page
        onSendToConfig: {
            designer_console.text += "i need sleep" + "\n"
            // view_module_name.text = msg

            // Uncomment when Cell model implemented
            view_module_name.text = cellID
            view_v_oc.value = v_oc
            view_i_sc.value = i_sc
            view_ref_temp.value = ref_temp
            view_ref_irrad.value = ref_irrad
            view_ideality_factor.value = ideality_factor
        }
    }
    

    GridLayout {
        anchors.fill: parent
        columns: 1
        rowSpacing: 0

        Rectangle {
            Layout.minimumHeight: parent.height * 0.3
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }
            color: "#222222"

            GridLayout {
                anchors.fill: parent
                columns: 2
                rows: 3
                
                Text {
                    text: "Configuration"
                    Layout.columnSpan: 2
                    Layout.alignment: Qt.AlignHCenter
                    color: "white"
                }
                Button {
                    id: load_config_button
                    text: "Load Configuration"
                    Layout.columnSpan: 1
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        writeToParent(6, config_name.text)
                    }
                }
                Button {
                    id: save_config_button
                    text: "Save Configuration"
                    Layout.columnSpan: 1
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        writeToParent(5, config_name.text)
                    }
                }
                TextField {
                    id: config_name
                    text: "new_config"
                    Layout.columnSpan: 2
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.4
            Layout.minimumWidth: parent.width
            border {
                width: 1
            } 
            
            TabBar {
                id: bar
                width: parent.width
                TabButton {
                    text: "Module Creator"
                }
                TabButton {
                    text: "Module Viewer"
                }
            }
            
            StackLayout {
                anchors {
                    top: bar.bottom
                    bottom: parent.bottom
                    left: parent.left
                    right: parent.right
                }
                currentIndex: bar.currentIndex
                Rectangle {
                    id: module_creator
                    color: "#222222"
                    property int i: 0
                    property var msg: ["uh oh, no cell"]
                    GridLayout {
                        id: creator_grid
                        columns: 6
                        rows: 5
                        anchors.fill: parent
                        GridLayout {
                            columns: 2
                            rows: 1
                            Layout.columnSpan: 6
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Layout.margins: 20
                            Text {
                                text: "Module Name: "
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            TextField {
                                id: module_name
                                text: "new_module"
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }

                        GridLayout {
                            id: v_oc_grid
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "OC Voltage"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: v_oc
                                wrap: false;
                                value: 0.721
                                from: 0.000
                                to: 1.000
                                decimals: 3
                                stepSize: 0.001
                                wheelEnabled: true
                            }
                        }
                        GridLayout {
                            id: i_sc_grid
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "SC Current"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: i_sc
                                wrap: false;
                                value: 6.15
                                from: 0.00
                                to: 10.00
                                stepSize: 0.01
                                wheelEnabled: true
                            }
                        }

                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Reference Temp (K)"
                                // Layout.fillWidth: true
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: ref_temp
                                wrap: false;
                                value: 298.15
                                from: 200.00
                                to: 400.00
                                decimals: 2
                                stepSize: 0.01
                                wheelEnabled: true
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Reference Irradiance (W/m^2)"
                                // Layout.fillWidth: true
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: ref_irrad
                                wrap: false;
                                value: 1000.0
                                from: 0.0
                                to: 2000.0
                                decimals: 1
                                stepSize: 0.1
                                wheelEnabled: true
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }

                        GridLayout {
                            id: if_grid
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Ideality Factor"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: ideality_factor
                                wrap: false;
                                value: 2.0
                                from: 0.0
                                to: 10.0
                                stepSize: 0.1
                                wheelEnabled: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                        Button {
                            id: create_button
                            text: "Create Module"
                            Layout.columnSpan: 3
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignHCenter
                            onClicked: {
                                module_creator.msg = [module_name.text + module_creator.i, "steelblue", v_oc.value, 
                                    i_sc.value, ref_temp.value, ref_irrad.value, ideality_factor.value]
                                module_creator.i++
                                // console.log(module_creator.msg)
                                designer_console.text += "added cell" + "\n"
                                pv_designer_controls_rect.writeToParent(1, module_creator.msg)
                                
                            }
                        }
                    }
                }
                Rectangle {
                    id: module_viewer
                    color: "#222222"
                    property var msg: ["uh oh, no cell"]
                    GridLayout {
                        id: viewer_grid
                        columns: 6
                        rows: 5
                        anchors.fill: parent

                        GridLayout {
                            columns: 2
                            rows: 1
                            Layout.columnSpan: 6
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Layout.margins: 20
                            Text {
                                text: "Module Name: "
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            TextField {
                                id: view_module_name
                                text: "No Module Selected"
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                                readOnly: true
                            }
                        }

                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "OC Voltage"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: view_v_oc
                                wrap: false;
                                value: 0.721
                                from: 0.000
                                to: 1.000
                                decimals: 3
                                stepSize: 0.001
                                wheelEnabled: true
                            }
                        }
                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "SC Current"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: view_i_sc
                                wrap: false;
                                value: 6.15
                                from: 0.00
                                to: 10.00
                                stepSize: 0.01
                                wheelEnabled: true
                            }
                        }

                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Reference Temp (K)"
                                // Layout.fillWidth: true
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: view_ref_temp
                                wrap: false;
                                value: 298.15
                                from: 200.00
                                to: 400.00
                                decimals: 2
                                stepSize: 0.01
                                wheelEnabled: true
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Reference Irradiance (W/m^2)"
                                // Layout.fillWidth: true
                                color: "white"
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: view_ref_irrad
                                wrap: false;
                                value: 1000.0
                                from: 0.0
                                to: 2000.0
                                decimals: 1
                                stepSize: 0.1
                                wheelEnabled: true
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }
                        GridLayout {
                            columns: 1
                            rows: 2
                            Layout.columnSpan: 3
                            Layout.fillHeight: true
                            Layout.alignment: Qt.AlignHCenter
                            Text {
                                text: "Ideality Factor"
                                color: "white"
                                // Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                            MLDoubleSpinBox {
                                id: view_ideality_factor
                                wrap: false;
                                value: 2.0
                                from: 0.0
                                to: 10.0
                                stepSize: 0.1
                                wheelEnabled: true
                                Layout.alignment: Qt.AlignHCenter
                            }
                        }

                        GridLayout {
                            columns: 2
                            rows: 1
                            Layout.columnSpan: 3
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignHCenter
                            
                            Button {
                                id: save_button
                                text: "Save Module"
                                Layout.columnSpan: 1
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                                onClicked: {
                                    module_viewer.msg = [view_module_name.text, "steelblue", view_v_oc.value, 
                                        view_i_sc.value, view_ref_temp.value, view_ref_irrad.value, view_ideality_factor.value]
                                    designer_console.text += "saved cell" + "\n"
                                    pv_designer_controls_rect.writeToParent(2, module_viewer.msg)
                                }
                            }
                            Button {
                                id: delete_button
                                text: "Delete Module"
                                Layout.columnSpan: 1
                                Layout.fillWidth: true
                                Layout.alignment: Qt.AlignHCenter
                                onClicked: {
                                    module_viewer.msg = view_module_name.text
                                    designer_console.text += "deleted cell" + "\n"
                                    pv_designer_controls_rect.writeToParent(3, module_viewer.msg)
                                }
                            }
                        }                        
                    }
                }
            }
        }

        Rectangle {
            Layout.minimumHeight: parent.height * 0.3
            Layout.minimumWidth: parent.width
            border {
                width: 1
            }

            color: "black"
            ScrollView {
                anchors.fill: parent

                TextArea {
                    id: designer_console
                    objectName: "console"
                    color: "white"
                    Layout.preferredWidth: parent.width
                    focus: true
                    wrapMode: Text.WordWrap
                    placeholderText: "TYPE COMMAND then CTRL+ENTER to use CLI."

                    Keys.onReturnPressed: (event) => {
                        if(event.modifiers & Qt.ControlModifier) {
                            text += '\n'
                            cursorPosition = text.length
                            // TODO: update backend
                            console.log("hi!")
                        }
                    }
                }
            }
        }
    }   
}
