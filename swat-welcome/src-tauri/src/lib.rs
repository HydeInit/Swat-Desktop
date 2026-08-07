// Static UI scaffold only - no commands yet. The install engine, catalog
// loading, and polkit-gated privileged steps are follow-up work (see
// issue #19), not part of this pass.
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
