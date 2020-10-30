import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import BloodPressure 0.1

Kirigami.Page
{
id: bloodpressurePage
title: qsTr("Blood Pressure Monitor")

    BloodPressure { // BloodPressure object registered at main.py
        id: bloodpressure
        onSetOK: {
            pageStack.pop() // Return to main monitor page once values are stored
        }
    }


    Kirigami.FormLayout {
        id: content
        anchors.fill: parent

        TextField {
            id: txtSystolic
            placeholderText: qsTr("Sys")
            maximumLength: 3
            font.pointSize: 50
            font.bold: true
            horizontalAlignment: TextInput.AlignHCenter
            background: Rectangle {
                implicitWidth: 40
                implicitHeight: 200
                }
            }

        TextField {
            id: txtDiastolic
            placeholderText: qsTr("Dia")
            maximumLength: 3
            font.pointSize: 50
            font.bold: true
            horizontalAlignment: TextInput.AlignHCenter
            background: Rectangle {
                implicitWidth: 40
                implicitHeight: 200
            }
        }

        TextField {
            id: txtRate
            placeholderText: qsTr("Rate")
            maximumLength: 3
            font.pointSize: 20
            font.bold: true
            horizontalAlignment: TextInput.AlignHCenter
            background: Rectangle {
                implicitWidth: 20
                implicitHeight: 100
            }
        }

        Button {
            id: buttonSetBP
            anchors.horizontalCenter: txtDiastolic.horizontalCenter
            anchors.top: txtRate.bottom
            text: qsTr("Done")
            flat: false
            onClicked: {
                bloodpressure.getvals(txtSystolic.text, txtDiastolic.text,
                                      txtRate.text);
            }

        }
    }
}
