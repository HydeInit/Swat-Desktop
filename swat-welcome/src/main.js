const { invoke } = window.__TAURI__.core;
const { listen } = window.__TAURI__.event;

const screens = Array.from(document.querySelectorAll("[data-screen]"));
const dots = Array.from(document.querySelectorAll(".dot"));
let current = 0;

const installsIndex = screens.findIndex((s) => s.id === "screen-installs");
const installingIndex = screens.findIndex((s) => s.id === "screen-installing");
const finishIndex = screens.findIndex((s) => s.id === "screen-finish");

const logEl = document.getElementById("install-log");
const progressEl = document.getElementById("install-progress");
const continueBtn = document.getElementById("installing-continue");
const finishSummaryEl = document.getElementById("finish-summary");

let catalogById = new Map();
let completedCount = 0;
let selectedTotal = 0;

function showScreen(index) {
  screens[current].hidden = true;
  dots[current].classList.remove("active");
  current = index;
  screens[current].hidden = false;
  dots[current].classList.add("active");
}

function renderCatalog(entries) {
  const panels = {
    browsers: document.querySelector('[data-tab-panel="browsers"]'),
    coding: document.querySelector('[data-tab-panel="coding"]'),
    ai: document.querySelector('[data-tab-panel="ai"]'),
  };

  for (const entry of entries) {
    catalogById.set(entry.id, entry);
    const panel = panels[entry.category];
    if (!panel) continue;

    const label = document.createElement("label");
    label.className = "catalog-item";
    label.innerHTML = `
      <input type="checkbox" data-app-id="${entry.id}" />
      <span>
        <span class="catalog-name">${entry.name}</span>
        <span class="catalog-desc">${entry.description}</span>
      </span>
    `;
    panel.appendChild(label);
  }
}

function selectedAppIds() {
  return Array.from(document.querySelectorAll("[data-app-id]:checked")).map(
    (input) => input.dataset.appId,
  );
}

function appendLog(line) {
  const div = document.createElement("div");
  div.className = "log-line";
  div.textContent = line;
  logEl.appendChild(div);
  logEl.scrollTop = logEl.scrollHeight;
}

function setFinishSummary(succeeded, failed) {
  if (selectedTotal === 0) {
    finishSummaryEl.textContent =
      "You can reopen SWAT Welcome any time from the applications menu to change your mind.";
    return;
  }
  const failedPart = failed.length ? `, ${failed.length} failed` : "";
  finishSummaryEl.textContent =
    `${succeeded.length} of ${selectedTotal} apps installed${failedPart}. ` +
    "You can reopen SWAT Welcome any time from the applications menu to change your mind.";
}

async function startInstall(appIds) {
  selectedTotal = appIds.length;
  completedCount = 0;
  logEl.innerHTML = "";
  progressEl.style.width = "0%";
  continueBtn.disabled = true;

  await invoke("run_install", { appIds });
}

listen("install:app-started", ({ payload }) => {
  const entry = catalogById.get(payload.app_id);
  appendLog(`Installing ${entry ? entry.name : payload.app_id}...`);
});

listen("install:log", ({ payload }) => {
  appendLog(payload.line);
});

listen("install:app-done", ({ payload }) => {
  completedCount += 1;
  progressEl.style.width = `${Math.round((completedCount / selectedTotal) * 100)}%`;
  if (!payload.success) {
    appendLog(`Failed: ${payload.error || "unknown error"}`);
  }
});

listen("install:finished", ({ payload }) => {
  continueBtn.disabled = false;
  setFinishSummary(payload.succeeded, payload.failed);
});

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.action;
    if (action === "next" && current === installsIndex) {
      const appIds = selectedAppIds();
      if (appIds.length === 0) {
        selectedTotal = 0;
        setFinishSummary([], []);
        showScreen(finishIndex);
      } else {
        showScreen(installingIndex);
        startInstall(appIds);
      }
    } else if (action === "next" && current < screens.length - 1) {
      showScreen(current + 1);
    } else if (action === "back" && current > 0) {
      showScreen(current - 1);
    } else if (action === "skip") {
      selectedTotal = 0;
      setFinishSummary([], []);
      showScreen(finishIndex);
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

invoke("get_catalog").then(renderCatalog);
