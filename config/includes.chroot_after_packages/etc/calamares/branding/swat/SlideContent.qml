import QtQuick 2.0
import io.calamares.core 1.0

Rectangle {
    anchors.fill: parent
    color: Branding.styleString( Branding.SidebarBackground )

    property alias title: titleText.text
    property alias body: bodyText.text
    property int titleSize: 22

    Column {
        anchors.centerIn: parent
        width: parent.width * 0.7
        spacing: 16

        Text {
            id: titleText
            width: parent.width
            color: Branding.styleString( Branding.SidebarBackgroundCurrent )
            font.pointSize: titleSize
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: bodyText
            width: parent.width
            color: Branding.styleString( Branding.SidebarText )
            font.pointSize: 12
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
    }
}
