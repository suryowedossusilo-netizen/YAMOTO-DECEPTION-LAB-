use serde_json::Value;
use std::{io::Write,process::{Command,Stdio}};
use tauri::Manager;
#[tauri::command]
fn engine_request(payload:Value,app:tauri::AppHandle)->Result<Value,String>{
 let data=app.path().app_data_dir().map_err(|e|e.to_string())?;std::fs::create_dir_all(&data).map_err(|e|e.to_string())?;
 let exe=app.path().resource_dir().ok().map(|p|p.join("yamoto-engine.exe")).filter(|p|p.exists()).or_else(||std::env::current_exe().ok().and_then(|p|p.parent().map(|d|d.join("yamoto-engine.exe"))).filter(|p|p.exists())).ok_or("Python engine executable not found in app resources")?;
 let mut child=Command::new(exe).env("YAMOTO_DATA_DIR",data).stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::piped()).spawn().map_err(|e|e.to_string())?;
 let bytes=serde_json::to_vec(&payload).map_err(|e|e.to_string())?;{let mut input=child.stdin.take().ok_or("stdin unavailable")?;input.write_all(&bytes).map_err(|e|e.to_string())?;}
 let output=child.wait_with_output().map_err(|e|e.to_string())?;if !output.status.success(){return Err(String::from_utf8_lossy(&output.stderr).to_string())}serde_json::from_slice(&output.stdout).map_err(|e|format!("Invalid engine JSON: {e}"))
}
pub fn run(){tauri::Builder::default().invoke_handler(tauri::generate_handler![engine_request]).run(tauri::generate_context!()).expect("failed to run YAMOTO DECEPTION LAB");}