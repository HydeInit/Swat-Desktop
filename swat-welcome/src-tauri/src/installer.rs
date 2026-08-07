use serde::{Deserialize, Serialize};
use std::process::Stdio;
use tauri::{AppHandle, Emitter};
use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;
use tokio::sync::mpsc;

const CATALOG_JSON: &str = include_str!("catalog.json");

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct CatalogEntry {
    pub id: String,
    pub name: String,
    pub description: String,
    pub category: String,
    pub install: InstallMethod,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum InstallMethod {
    Apt {
        package: String,
    },
    AptRepo {
        key_url: String,
        repo_line: String,
        package: String,
    },
    Script {
        command: String,
        args: Vec<String>,
        privileged: bool,
    },
    Flatpak {
        remote: String,
        app_id: String,
    },
}

fn load_catalog() -> Vec<CatalogEntry> {
    serde_json::from_str(CATALOG_JSON).expect("catalog.json must be valid")
}

#[tauri::command]
pub fn get_catalog() -> Vec<CatalogEntry> {
    load_catalog()
}

#[derive(Clone, Serialize)]
struct AppStarted<'a> {
    app_id: &'a str,
    index: usize,
    total: usize,
}

#[derive(Clone, Serialize)]
struct LogLine<'a> {
    app_id: &'a str,
    line: String,
}

#[derive(Clone, Serialize)]
struct AppDone<'a> {
    app_id: &'a str,
    success: bool,
    error: Option<String>,
}

#[derive(Clone, Serialize)]
struct Finished {
    succeeded: Vec<String>,
    failed: Vec<String>,
}

#[tauri::command]
pub async fn run_install(app_handle: AppHandle, app_ids: Vec<String>) -> Result<(), String> {
    let catalog = load_catalog();
    let total = app_ids.len();
    let mut succeeded = Vec::new();
    let mut failed = Vec::new();

    for (index, app_id) in app_ids.iter().enumerate() {
        let Some(entry) = catalog.iter().find(|e| &e.id == app_id) else {
            failed.push(app_id.clone());
            continue;
        };

        let _ = app_handle.emit(
            "install:app-started",
            AppStarted { app_id, index, total },
        );

        match run_one(&app_handle, app_id, &entry.install).await {
            Ok(()) => {
                succeeded.push(app_id.clone());
                let _ = app_handle.emit(
                    "install:app-done",
                    AppDone { app_id, success: true, error: None },
                );
            }
            Err(e) => {
                failed.push(app_id.clone());
                let _ = app_handle.emit(
                    "install:app-done",
                    AppDone { app_id, success: false, error: Some(e) },
                );
            }
        }
    }

    let _ = app_handle.emit("install:finished", Finished { succeeded, failed });
    Ok(())
}

async fn run_one(app_handle: &AppHandle, app_id: &str, method: &InstallMethod) -> Result<(), String> {
    let (program, args): (&str, Vec<String>) = match method {
        InstallMethod::Apt { package } => (
            "pkexec",
            vec!["apt-get".into(), "install".into(), "-y".into(), package.clone()],
        ),
        InstallMethod::AptRepo { key_url, repo_line, package } => {
            // One pkexec prompt for the whole key+repo+update+install sequence,
            // rather than one prompt per step.
            let script = format!(
                "set -e; \
                 curl -fsSL {key_url} | gpg --dearmor -o /etc/apt/keyrings/{app_id}.gpg; \
                 echo '{repo_line}' > /etc/apt/sources.list.d/{app_id}.list; \
                 apt-get update; \
                 apt-get install -y {package}"
            );
            ("pkexec", vec!["bash".into(), "-c".into(), script])
        }
        InstallMethod::Flatpak { remote, app_id: flatpak_id } => (
            "flatpak",
            vec!["install".into(), "-y".into(), remote.clone(), flatpak_id.clone()],
        ),
        InstallMethod::Script { command, args, privileged } => {
            if *privileged {
                let mut full = vec![command.clone()];
                full.extend(args.clone());
                ("pkexec", full)
            } else {
                (command.as_str(), args.clone())
            }
        }
    };

    stream_command(app_handle, app_id, program, &args).await
}

async fn stream_command(
    app_handle: &AppHandle,
    app_id: &str,
    program: &str,
    args: &[String],
) -> Result<(), String> {
    let mut child = Command::new(program)
        .args(args)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("failed to start {program}: {e}"))?;

    let stdout = child.stdout.take().expect("stdout was piped");
    let stderr = child.stderr.take().expect("stderr was piped");

    // Both streams feed one channel so lines are emitted in the order they
    // actually arrive, and the receive loop ends cleanly once both reader
    // tasks finish and drop their sender halves.
    let (tx, mut rx) = mpsc::unbounded_channel::<String>();

    let tx_out = tx.clone();
    let out_task = tokio::spawn(async move {
        let mut lines = BufReader::new(stdout).lines();
        while let Ok(Some(line)) = lines.next_line().await {
            let _ = tx_out.send(line);
        }
    });

    let err_task = tokio::spawn(async move {
        let mut lines = BufReader::new(stderr).lines();
        while let Ok(Some(line)) = lines.next_line().await {
            let _ = tx.send(line);
        }
    });

    while let Some(line) = rx.recv().await {
        let _ = app_handle.emit("install:log", LogLine { app_id, line });
    }

    let _ = out_task.await;
    let _ = err_task.await;

    let status = child.wait().await.map_err(|e| e.to_string())?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("{program} exited with {status}"))
    }
}
