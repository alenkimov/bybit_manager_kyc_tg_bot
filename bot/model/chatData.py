from typing import Dict, List, TypedDict, Any

chat_data = {}


class ChatDataEntry(TypedDict):
    accounts: Dict[str, Any]
    bad: List[str]


ChatData = Dict[str, ChatDataEntry]
