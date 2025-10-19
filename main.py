import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agents.planner_agent import planner_agent
import json

if __name__ == "__main__":
    user_query = "Tìm bài IELTS Reading về Love and Relationships"
    print(f"Query: {user_query}")
    print("=" * 70)
    result = planner_agent(user_query)
    print("\n=== Kết quả ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
