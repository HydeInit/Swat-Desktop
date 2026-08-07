const screens = Array.from(document.querySelectorAll("[data-screen]"));
const dots = Array.from(document.querySelectorAll(".dot"));
let current = 0;

function showScreen(index) {
  screens[current].hidden = true;
  dots[current].classList.remove("active");
  current = index;
  screens[current].hidden = false;
  dots[current].classList.add("active");
}

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    if (action === "next" && current < screens.length - 1) {
      showScreen(current + 1);
    } else if (action === "back" && current > 0) {
      showScreen(current - 1);
    } else if (action === "skip") {
      showScreen(screens.length - 1);
    } else if (action === "close") {
      window.__TAURI__.window.getCurrentWindow().close().catch(console.error);
    }
  });
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
      panel.hidden = true;
    });
    tab.classList.add("active");
    document.querySelector(`[data-tab-panel="${tab.dataset.tab}"]`).hidden = false;
  });
});
