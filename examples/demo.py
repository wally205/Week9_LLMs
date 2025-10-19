import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.planner_agent import planner_agent
import json

if __name__ == "__main__":
    # Test với topic không có trong DB
    user_query = "Tìm bài IELTS Reading về Love and Relationships"
    
    print(f"Query: {user_query}")
    print("=" * 70)
    
    result = planner_agent(user_query)
    
    print("\n=== Kết quả (JSON format) ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("💡 Lưu ý:")
    print("- Demo đang sử dụng Gemini API (models/gemini-2.5-flash)")
    print("- API key được load từ file .env")
    print("- Nội dung snippet & summary được generate bởi Gemini AI")

