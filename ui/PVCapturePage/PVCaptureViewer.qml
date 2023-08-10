import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtCharts
import "../GraphSet"

/*
    Characterization Viewer
        Source Characteristics
        I-V, P-V Curves
*/

Rectangle {
    anchors {
        top: parent.top
        bottom: parent.bottom
        left: pv_cap_controls.right
        right: parent.right
    }
    anchors.margins: 15


    GridLayout {
        anchors.fill: parent
        columns: 2
        rowSpacing: 0
        columnSpacing: 0

        GraphSet {
            id: chars
            Layout.minimumHeight: parent.height * 0.75
            Layout.minimumWidth: parent.width
            Layout.columnSpan: 2
            property var model:
                ListModel {
                    ListElement { key: "I_V"; chart_title: "I-V Curve" }
                    ListElement { key: "P_V"; chart_title: "P-V Curve" }
                    ListElement { key: "IV_CMP"; chart_title: "I-V Curve Comparison Against Other Cells" }
                    ListElement { key: "FF_CMP"; chart_title: "FF Comparison Against Other Cells" }
                    ListElement { key: "PMPP_CMP"; chart_title: "P<sub>MPP</sub> Comparison Against Other Cells" }
                    ListElement { key: "CLUSTER"; chart_title: "Clustering Against Other Cells" }
                }
        }

        Repeater {
            id : rep
            model: [
                { title: "V<sub>OC</sub> (V)"   , ref: "v_oc"  },
                { title: "I<sub>SC</sub> (A)"   , ref: "i_sc"  },
                { title: "V<sub>MPP</sub> (V)"  , ref: "v_mpp" },
                { title: "I<sub>MPP</sub> (A)"  , ref: "i_mpp" },
                { title: "P<sub>MPP</sub> (W)"  , ref: "p_mpp" },
                { title: "FF (%)"               , ref: "ff"    },
                { title: "Percentile Perf"      , ref: "pp"    },
            ]
            Rectangle {
                Layout.preferredHeight: (parent.height - chars.height) / Math.ceil(rep.count / 2)
                Layout.minimumWidth: parent.width * 0.5
                Layout.columnSpan: 1

                RowLayout {
                    anchors.fill: parent

                    Label {
                        Layout.minimumHeight: parent.height
                        Layout.minimumWidth: parent.width * 0.5
                        horizontalAlignment: Text.AlignRight
                        color: "black"
                        textFormat: Text.RichText
                        text: modelData.title + ": "
                    }

                    Label {
                        objectName: modelData.ref
                        Layout.minimumHeight: parent.height
                        Layout.minimumWidth: parent.width * 0.5
                        color: "grey"
                        text: "N/A"
                    }
                }
            }
        }
    }
}
