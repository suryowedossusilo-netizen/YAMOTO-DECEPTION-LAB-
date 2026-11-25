"""Local JSON request engine for YAMOTO DECEPTION LAB. No deception inference is implemented."""
import json,os,sqlite3,sys
from pathlib import Path
from datetime import datetime,timezone
VERSION="0.2.0"
SCHEMA="""PRAGMA foreign_keys=ON; CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY,created_at TEXT NOT NULL,kind TEXT NOT NULL,source_name TEXT,duration_seconds REAL,notes TEXT DEFAULT ''); CREATE TABLE IF NOT EXISTS datasets(id INTEGER PRIMARY KEY,name TEXT NOT NULL,description TEXT DEFAULT '',created_at TEXT NOT NULL,participant_count INTEGER DEFAULT 0,label_scheme TEXT DEFAULT ''); CREATE TABLE IF NOT EXISTS experiments(id INTEGER PRIMARY KEY,name TEXT NOT NULL,dataset_id INTEGER,model_type TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'NOT TRAINED',created_at TEXT NOT NULL,result_json TEXT DEFAULT '{}');"""
def db_path():
 root=Path(os.environ.get("YAMOTO_DATA_DIR",Path.home()/".local"/"share"/"YamotoDeceptionLab"));root.mkdir(parents=True,exist_ok=True);return root/"yamoto.sqlite3"
def connect():
 c=sqlite3.connect(db_path());c.row_factory=sqlite3.Row;c.executescript(SCHEMA);return c
def now():return datetime.now(timezone.utc).isoformat()
def handle(q):
 a=q.get("action")
 if a=="health":
  with connect():pass
  return {"ok":True,"version":VERSION,"database":"READY","model_status":"NOT TRAINED"}
 if a=="dashboard":
  with connect() as c:return {"ok":True,**{k:c.execute("select count(*) from "+t).fetchone()[0] for k,t in [("sessions","sessions"),("datasets","datasets"),("experiments","experiments")]},"model_status":"NOT TRAINED"}
 if a in ("create_dataset","create_experiment"):
  name=str(q.get("name","")).strip()
  if not name:return {"ok":False,"error":"Name is required"}
  with connect() as c:
   if a=="create_dataset":cur=c.execute("insert into datasets(name,description,created_at) values(?,?,?)",(name,str(q.get("description","")),now()))
   else:cur=c.execute("insert into experiments(name,model_type,status,created_at) values(?,?,?,?)",(name,str(q.get("model_type","baseline")),"NOT TRAINED",now()))
   return {"ok":True,"id":cur.lastrowid}
 if a in ("list_datasets","list_experiments","list_sessions"):
  table={"list_datasets":"datasets","list_experiments":"experiments","list_sessions":"sessions"}[a]
  with connect() as c:return {"ok":True,"items":[dict(r) for r in c.execute("select * from "+table+" order by id desc limit 200")]}
 return {"ok":False,"error":"Unsupported action: "+str(a)}
if __name__=="__main__":
 try:print(json.dumps(handle(json.loads(sys.stdin.read() or "{}")),ensure_ascii=False),flush=True)
 except Exception as e:print(json.dumps({"ok":False,"error":str(e)}),flush=True)