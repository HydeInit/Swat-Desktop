import QtQuick 2.0
import calamares.slideshow 1.0

Presentation
{
    id: presentation

    Slide {
        Image {
            source: "welcome.png"
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
        }
    }

    function nextSlide() {
        presentation.goToNextSlide()
    }

    Timer {
        interval: 1000000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.nextSlide()
    }
}
