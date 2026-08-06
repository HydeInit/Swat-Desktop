// QML navigation: traditional bottom bar, text-only Back/Next/Cancel -
// no icon assets, keeps this self-contained. API verified against
// Calamares' kaos_branding reference (ViewManager.back()/next()/quit(),
// backEnabled/nextEnabled/quitEnabled/quitVisible/backAndNextVisible),
// simplified from their version by dropping the About/Debug buttons
// (About needs a separate about.qml this branding doesn't have).
import io.calamares.ui 1.0
import io.calamares.core 1.0

import QtQuick 2.3
import QtQuick.Layouts 1.3

Rectangle {
    id: navigationBar
    color: Branding.styleString( Branding.SidebarBackground )
    width: parent.width
    height: 56

    RowLayout {
        anchors.fill: parent
        anchors.margins: 8
        spacing: 8

        Item {
            Layout.fillWidth: true
        }

        Rectangle {
            id: cancelArea
            width: 90
            height: 36
            radius: 3
            color: "transparent"
            border.color: Branding.styleString( Branding.SidebarText )
            border.width: 1
            visible: ViewManager.quitVisible && ( ViewManager.currentStepIndex < ViewManager.rowCount() - 1 )
            enabled: ViewManager.quitEnabled

            MouseArea {
                id: mouseCancel
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true
                onClicked: { ViewManager.quit(); }
            }

            Text {
                anchors.centerIn: parent
                text: qsTr("Cancel")
                color: Branding.styleString( mouseCancel.containsMouse ? Branding.SidebarTextCurrent : Branding.SidebarText )
                font.pointSize: 10
            }
        }

        Rectangle {
            id: backArea
            width: 90
            height: 36
            radius: 3
            color: "transparent"
            border.color: Branding.styleString( Branding.SidebarText )
            border.width: 1
            visible: ViewManager.backAndNextVisible
            enabled: ViewManager.backEnabled

            MouseArea {
                id: mouseBack
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true
                onClicked: { ViewManager.back(); }
            }

            Text {
                anchors.centerIn: parent
                text: qsTr("Back")
                color: Branding.styleString( !backArea.enabled ? Branding.SidebarBackgroundCurrent : ( mouseBack.containsMouse ? Branding.SidebarTextCurrent : Branding.SidebarText ) )
                font.pointSize: 10
            }
        }

        Rectangle {
            id: nextArea
            width: 90
            height: 36
            radius: 3
            color: Branding.styleString( Branding.SidebarBackgroundCurrent )
            visible: ViewManager.backAndNextVisible
            enabled: ViewManager.nextEnabled

            MouseArea {
                id: mouseNext
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true
                onClicked: { ViewManager.next(); }
            }

            Text {
                anchors.centerIn: parent
                text: qsTr("Next")
                color: Branding.styleString( Branding.SidebarTextCurrent )
                font.pointSize: 10
                opacity: nextArea.enabled ? 1 : 0.4
            }
        }
    }
}
