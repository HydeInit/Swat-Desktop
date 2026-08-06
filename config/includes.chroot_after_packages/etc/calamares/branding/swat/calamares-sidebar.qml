// QML sidebar: traditional vertical layout (left), one row per
// installer step, current step highlighted. API and property names
// (ViewManager, Branding.styleString, SidebarBackground/Text/*Current)
// verified against Calamares' own kaos_branding reference
// (calamares/calamares-extensions), adapted here to a vertical column
// instead of their horizontal layout, to match the layout users already
// saw in v0.1.0's widget-mode sidebar.
import io.calamares.ui 1.0
import io.calamares.core 1.0

import QtQuick 2.3
import QtQuick.Layouts 1.3

Rectangle {
    id: sideBar
    color: Branding.styleString( Branding.SidebarBackground )
    width: 190
    height: parent.height

    // Icon per step, indexed to match the fixed module order in
    // settings.conf's "show:" sequence (welcome, locale, keyboard,
    // partition, users, summary, then the exec/install progress step,
    // then finished). Positional, not name-based - ViewManager's model
    // doesn't expose a module-name role, only index and display text.
    property var stepIcons: [
        "icons/welcome.svg",
        "icons/locale.svg",
        "icons/keyboard.svg",
        "icons/partition.svg",
        "icons/users.svg",
        "icons/summary.svg",
        "icons/install.svg",
        "icons/finished.svg"
    ]

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 0
        spacing: 0

        Image {
            Layout.topMargin: 24
            Layout.bottomMargin: 24
            Layout.alignment: Qt.AlignHCenter
            width: 64
            height: 64
            source: "file:/" + Branding.imagePath(Branding.ProductLogo)
            sourceSize.width: width
            sourceSize.height: height
        }

        Repeater {
            model: ViewManager
            Rectangle {
                Layout.fillWidth: true
                height: 44
                color: Branding.styleString( index == ViewManager.currentStepIndex ? Branding.SidebarBackgroundCurrent : Branding.SidebarBackground )

                Image {
                    id: stepIcon
                    anchors.verticalCenter: parent.verticalCenter
                    x: 16
                    width: 20
                    height: 20
                    sourceSize.width: width
                    sourceSize.height: height
                    source: index < sideBar.stepIcons.length ? sideBar.stepIcons[index] : ""
                }

                Text {
                    anchors.verticalCenter: parent.verticalCenter
                    x: 48
                    color: Branding.styleString( index == ViewManager.currentStepIndex ? Branding.SidebarTextCurrent : Branding.SidebarText )
                    text: display
                    font.pointSize: index == ViewManager.currentStepIndex ? 11 : 10
                }
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}
