import json
from pathlib import Path


def _load_db(db_path: str | Path) -> list[dict]:
    p = Path(db_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("db.json must be a list of records")
    return data


def _search_reading(topic: str | None, db_path: str | Path = "data/db.json") -> list[dict]:
    data = _load_db(db_path)
    topic_l = (topic or "").lower()
    return [r for r in data if topic_l == str(r.get("topic", "")).lower() or not topic]


def handle_a2a_message(msg):
    params = msg.get("params", {})
    topic = params.get("topic")
    print(f"[Data Agent] Searching IELTS reading on topic: {topic}")

    # db.json is now in data/ folder
    db_path = Path(__file__).parent.parent / "data" / "db.json"
    result = _search_reading(topic, db_path=db_path)
    return {"records": result}