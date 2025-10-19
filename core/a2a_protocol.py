from agents.research_agent import handle_a2a_message as research_handler
from agents.data_agent import handle_a2a_message as data_handler


def send_a2a_message(msg):
    receiver = msg.get("receiver")
    if receiver == "research":
        return research_handler(msg)
    if receiver == "data":
        return data_handler(msg)
    return {"error": "unknown receiver"}
