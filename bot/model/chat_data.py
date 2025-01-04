from typing import TypedDict
from typing import Literal

from api_client.dto.accounts_by_telegram_dto import AccountByKycProviderDto

chat_data = {}


class AccountData(TypedDict):
    account: AccountByKycProviderDto
    link: str


class ChatDataEntry(TypedDict):
    accounts: dict[str, AccountData]  # {database_id: AccountData}
    bad: list[str]
    delayed: list[str]


ChatData = list[tuple[str, ChatDataEntry]]
