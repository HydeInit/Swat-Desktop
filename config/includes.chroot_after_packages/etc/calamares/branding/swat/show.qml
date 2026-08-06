import QtQuick 2.0
import calamares.slideshow 1.0

Presentation
{
    id: presentation

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#0a0e14"
            Column {
                anchors.centerIn: parent
                width: parent.width * 0.7
                spacing: 16
                Text {
                    width: parent.width
                    text: "SWAT"
                    color: "#00d4ff"
                    font.pointSize: 32
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    width: parent.width
                    text: "Streamlined Workstation, Advanced Tooling"
                    color: "#c5d1de"
                    font.pointSize: 14
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#0a0e14"
            Column {
                anchors.centerIn: parent
                width: parent.width * 0.7
                spacing: 16
                Text {
                    width: parent.width
                    text: "Built for development"
                    color: "#00d4ff"
                    font.pointSize: 22
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    width: parent.width
                    text: "Curated developer tooling out of the box - git, build-essential, ripgrep, fd-find, fzf, jq, and more - no post-install setup required."
                    color: "#c5d1de"
                    font.pointSize: 12
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#0a0e14"
            Column {
                anchors.centerIn: parent
                width: parent.width * 0.7
                spacing: 16
                Text {
                    width: parent.width
                    text: "Lean by design"
                    color: "#00d4ff"
                    font.pointSize: 22
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    width: parent.width
                    text: "A lightweight XFCE desktop and a sane, curated package selection - sensible defaults, no unnecessary cruft."
                    color: "#c5d1de"
                    font.pointSize: 12
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }

    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#0a0e14"
            Column {
                anchors.centerIn: parent
                width: parent.width * 0.7
                spacing: 16
                Text {
                    width: parent.width
                    text: "Built on Debian"
                    color: "#00d4ff"
                    font.pointSize: 22
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    width: parent.width
                    text: "A remaster of Debian 13 (trixie), with non-free firmware included for real-world WiFi, GPU, and audio hardware support."
                    color: "#c5d1de"
                    font.pointSize: 12
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }

    function nextSlide() {
        presentation.goToNextSlide()
    }

    Timer {
        interval: 8000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.nextSlide()
    }
}
