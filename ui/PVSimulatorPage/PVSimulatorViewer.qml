import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts
import "../GraphSet"

/*
    Simulation Viewer
        Source Characteristics
        MPPT Characteristics
        MPPT VREF Over PV I-V, P-V Curve Cross-section
        System Efficiency
*/


Rectangle {
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: pv_sim_controls.right
        right: parent.right
    }
    anchors.margins: 15


    GridLayout {
        anchors.fill: parent
        columns: 2
        rowSpacing: 0
        columnSpacing: 0

        GraphSet {
            property var model:
                ListModel {
                    ListElement { key: "I_SC"; chart_title: "I<sub>SC</sub> Over Time" }
                    ListElement { key: "V_OC"; chart_title: "V<sub>OC</sub> Over Time" }
                    ListElement { key: "V_MPP"; chart_title: "V<sub>MPP</sub> Over Time" }
                    ListElement { key: "I_MPP"; chart_title: "I<sub>MPP</sub> Over Time" }
                    ListElement { key: "P_MPP"; chart_title: "P<sub>MPP</sub> Over Time" }
                    ListElement { key: "IRRAD"; chart_title: "IRRAD Over Time" }
                    ListElement { key: "TEMP"; chart_title: "TEMP Over Time" }
                }
        }

        GraphSet {
            property var model:
                ListModel {
                    ListElement { key: "V_REF"; chart_title: "V<sub>REF</sub> On I-V/P-V Cross Section" }
                }
        }

        GraphSet {
            property var model:
                ListModel {
                    ListElement { key: "V_IN"; chart_title: "V<sub>IN</sub> Over Time" }
                    ListElement { key: "V_OUT"; chart_title: "V<sub>OUT</sub> Over Time" }
                    ListElement { key: "I_IN"; chart_title: "I<sub>IN</sub> Over Time" }
                    ListElement { key: "I_OUT"; chart_title: "I<sub>OUT</sub> Over Time" }
                    ListElement { key: "P_TRAN"; chart_title: "P<sub>TRANSFER</sub> Over Time" }
                    ListElement { key: "P_LOSS"; chart_title: "P<sub>LOSS</sub> Over Time" }
                }
        }

        GraphSet {
            property var model:
                ListModel {
                    ListElement { key: "PV_EFF"; chart_title: "PV Output EFF Over Time" }
                    ListElement { key: "MPPT_EFF"; chart_title: "MPPT Transfer EFF Over Time" }
                    ListElement { key: "TOT_EFF"; chart_title: "SYS EFF Over Time" }
                    ListElement { key: "TRAC_EFF"; chart_title: "Tracking EFF Over Time" }
                }
        }
    }
}
