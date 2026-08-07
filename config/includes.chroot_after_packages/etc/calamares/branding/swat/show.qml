import QtQuick 2.0
import calamares.slideshow 1.0

Presentation
{
    id: presentation

    Slide {
        SlideContent {
            title: "SWAT"
            titleSize: 32
            body: "Streamlined Workstation, Advanced Tooling"
        }
    }

    Slide {
        SlideContent {
            title: "Built for development"
            body: "Curated developer tooling out of the box - git, build-essential, ripgrep, fd-find, fzf, jq, and more - no post-install setup required."
        }
    }

    Slide {
        SlideContent {
            title: "Lean by design"
            body: "A lightweight XFCE desktop and a sane, curated package selection - sensible defaults, no unnecessary cruft."
        }
    }

    Slide {
        SlideContent {
            title: "Built on Debian"
            body: "A remaster of Debian 13 (trixie), with non-free firmware included for real-world WiFi, GPU, and audio hardware support."
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
