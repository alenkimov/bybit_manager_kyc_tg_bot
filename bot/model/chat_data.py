from typing import TypedDict
from typing import Literal

from api_client.dto.account_dto import AccountDto

chat_data = {}

AccountType = Literal["account"]


class AccountData(TypedDict):
    account: AccountDto
    link: str


class ChatDataEntry(TypedDict):
    accounts: dict[str, AccountData]  # {database_id: AccountData}
    bad: list[str]


ChatData = list[tuple[str, ChatDataEntry]]
