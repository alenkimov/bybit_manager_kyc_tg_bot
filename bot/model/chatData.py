from typing import Dict, List, Dict, Any
from APIClient.dto.account_dto import AccountDto

chat_data = {}


class ChatDataEntry(Dict):
    accounts: Dict[str, Dict["account", AccountDto]]
    bad: List[str]


ChatData = Dict[str, ChatDataEntry]
