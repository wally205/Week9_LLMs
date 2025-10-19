from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

with open("db.json", "r", encoding="utf-8") as f:
    IELTS_DATA = json.load(f)

class MCPRequest(BaseModel):
    method: str
    params: dict

@app.post("/ielts_db_tool")
def handle_mcp(req: MCPRequest):
    if req.method == "db.search_reading":
        topic = req.params.get("topic", "").lower()
        print(f"[IELTS DB Tool] Searching for readings on topic: {topic}")
        
        results = [entry for entry in IELTS_DATA if topic in entry["topic"].lower()]
        
        return {"results": results}
    else:
        return {"error": "Unknown method"}