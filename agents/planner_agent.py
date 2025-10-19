from core.a2a_protocol import send_a2a_message
import re


def _extract_topic(query: str) -> str:
    """Extract topic from user query."""
    query_lower = query.lower()
    
    # Danh sách topic có trong db.json
    known_topics = [
        "science", "astronomy", "biology", "technology", "transport", 
        "psychology", "environment", "archaeology", "business", "history",
        "education", "politics", "linguistics", "neuroscience", "health"
    ]
    
    # Tìm topic match
    for topic in known_topics:
        if topic in query_lower:
            return topic
    
    # Nếu không tìm thấy, trích xuất từ query
    # Bỏ stopwords và lấy tất cả keywords quan trọng
    stopwords = ["tìm", "bài", "ielts", "reading", "về", "find", "about", "on", "and", "the"]
    words = re.findall(r'\w+', query_lower)
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    
    # Trả về cụm từ hoàn chỉnh thay vì từ đầu tiên
    if keywords:
        # Lấy 2-3 từ đầu tiên để tạo topic phức hợp
        return " ".join(keywords[:3]) if len(keywords) > 1 else keywords[0]
    
    return "general"


def planner_agent(user_query):
    print(f"[Planner] Received: {user_query}")

    # Nếu user hỏi về "IELTS reading", thử Data Agent trước
    if "ielts" in user_query.lower() or "reading" in user_query.lower():
        topic = _extract_topic(user_query)
        
        # Gọi Data Agent tìm trong db.json
        msg = {
            "sender": "planner",
            "receiver": "data",
            "intent": "fetch_ielts_reading",
            "params": {"topic": topic}
        }
        result = send_a2a_message(msg)
        
        # Nếu Data Agent trả về rỗng → fallback sang Research Agent
        if not result.get("records"):
            print(f"[Planner] No local data found for '{topic}', querying Research Agent...")
            research_msg = {
                "sender": "planner",
                "receiver": "research",
                "intent": "collect_info",
                "params": {"topic": topic}
            }
            research_result = send_a2a_message(research_msg)
            # Kết hợp kết quả
            return {
                "source": "research_agent",
                "topic": topic,
                "message": f"No local IELTS materials found for '{topic}'. Here are external resources:",
                **research_result
            }
        
        return result
    
    # Ngược lại, giao cho Research Agent
    msg = {
        "sender": "planner",
        "receiver": "research",
        "intent": "collect_info",
        "params": {"topic": user_query}
    }
    return send_a2a_message(msg)
