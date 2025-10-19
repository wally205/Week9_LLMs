import os
from pathlib import Path

# Load .env file if exists
try:
    from dotenv import load_dotenv
    # .env is in project root, not in agents/
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[Research Agent] Loaded API key from .env file")
    else:
        print(f"[Research Agent] .env file not found at {env_path}")
except ImportError:
    pass  # python-dotenv not installed, will use environment variables only


def _generate_snippet_with_gemini(topic: str, title: str, context: str = "") -> str:
    """Use Gemini to generate a realistic IELTS reading snippet."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            # Sử dụng gemini-2.5-flash (stable version, free tier)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            prompt = (
                f"Generate a 2-3 sentence IELTS Reading passage snippet about '{topic}'. "
                f"{context} "
                f"Write in academic style suitable for IELTS Band 7+. "
                f"Make it unique and different from other passages on the same topic."
            )
            resp = model.generate_content(prompt)
            text = getattr(resp, "text", None)
            if isinstance(text, str) and text.strip():
                return text.strip()
        except Exception as e:
            print(f"[Research Agent] Gemini API error: {e}")
    
    # Fallback: Tạo snippet chi tiết hơn dựa trên topic
    return (
        f"This IELTS Reading passage explores {topic}, examining various perspectives and providing "
        f"detailed analysis of key themes. The text includes academic vocabulary, complex sentence "
        f"structures, and requires careful comprehension skills typical of Band 7+ materials."
    )


def _web_search(topic: str):
    """Return IELTS Reading resources with Gemini-generated snippets."""
    q = (topic or "").strip().lower()
    
    # Real IELTS Reading resources với context khác nhau
    base_resources = [
        {
            "title": f"IELTS Reading: {q.title()} - British Council",
            "url": "https://learnenglish.britishcouncil.org/skills/reading",
            "context": "Focus on cultural and social perspectives.",
        },
        {
            "title": f"IELTS {q.title()} Reading Practice - IDP IELTS",
            "url": "https://www.ielts.org/for-test-takers/sample-test-questions",
            "context": "Focus on scientific research and psychological factors.",
        },
        {
            "title": f"Academic Reading on {q.title()} - IELTS Liz",
            "url": "https://ieltsliz.com/ielts-reading-tips/",
            "context": "Focus on academic analysis and theoretical frameworks.",
        },
    ]
    
    # Generate snippets using Gemini with different contexts
    results = []
    for resource in base_resources:
        snippet = _generate_snippet_with_gemini(
            q, 
            resource["title"], 
            context=resource["context"]
        )
        results.append({
            "title": resource["title"],
            "url": resource["url"],
            "snippet": snippet
        })
    
    return results


def _summarize(texts: list[str]) -> str:
    """Summarize texts using Gemini with fallback."""
    joined = " ".join(t for t in texts if t)
    if not joined:
        return "No content to summarize."

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            # Sử dụng gemini-2.5-flash (stable version, free tier)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            prompt = (
                "Summarize the following IELTS reading content into a concise paragraph. "
                "Focus on key facts, balanced arguments, and academic insights suitable for IELTS preparation.\n\n" + joined
            )
            resp = model.generate_content(prompt)
            text = getattr(resp, "text", None)
            if isinstance(text, str) and text.strip():
                return text.strip()
        except Exception as e:
            print(f"[Research Agent] Gemini API error in summarize: {e}")

    # Fallback: Tóm tắt thông minh hơn, không lặp lại
    sentences = joined.split('. ')
    unique_sentences = []
    seen = set()
    for s in sentences:
        s_clean = s.strip().lower()[:50]  # So sánh 50 ký tự đầu
        if s_clean not in seen and s.strip():
            seen.add(s_clean)
            unique_sentences.append(s.strip())
    
    # Lấy 2-3 câu đầu tiên, không trùng lặp
    summary_text = '. '.join(unique_sentences[:3])
    return summary_text + ('.' if not summary_text.endswith('.') else '')


def handle_a2a_message(msg):
    params = msg.get("params", {})
    intent = msg.get("intent")
    if intent == "collect_info":
        topic = params.get("topic")
        print(f"[Research Agent] Collecting info for: {topic}")
        results = _web_search(topic)
        summary = _summarize([r["snippet"] for r in results])
        return {"results": results, "summary": summary}
    return {"error": "unknown intent"}
