import json,os,subprocess,sys
from pathlib import Path
ENGINE=Path(__file__).parents[1]/"engine"/"yamoto_engine.py"
def call(tmp_path,action,**kw):
 env=os.environ.copy();env["YAMOTO_DATA_DIR"]=str(tmp_path)
 p=subprocess.run([sys.executable,str(ENGINE)],input=json.dumps({"action":action,**kw}),text=True,capture_output=True,env=env,check=True)
 return json.loads(p.stdout)
def test_health(tmp_path):
 r=call(tmp_path,"health");assert r["ok"] and r["model_status"]=="NOT TRAINED"
def test_dataset_create_and_list(tmp_path):
 assert call(tmp_path,"create_dataset",name="Pilot")["ok"]
 assert call(tmp_path,"list_datasets")["items"][0]["name"]=="Pilot"
def test_experiment_stays_untrained(tmp_path):
 assert call(tmp_path,"create_experiment",name="Baseline")["ok"]
 assert call(tmp_path,"list_experiments")["items"][0]["status"]=="NOT TRAINED"
